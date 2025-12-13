//! Benchmarks for pf-workflow-core.
//!
//! Run with: cargo bench -p pf-workflow-core

use criterion::{black_box, criterion_group, criterion_main, BenchmarkId, Criterion, Throughput};
use pf_workflow_core::{
    CancellationToken, ExecutionContext, ExecutorConfig, ResourceHint, Result, Step, StepMetrics,
    StepResult, WorkflowExecutor,
};
use serde_json::Value;
use std::time::Duration;

// ============================================================================
// Benchmark Steps
// ============================================================================

/// A minimal step for overhead measurement.
struct MinimalStep {
    id: String,
}

impl MinimalStep {
    fn new(id: &str) -> Self {
        Self { id: id.to_string() }
    }
}

impl Step for MinimalStep {
    fn id(&self) -> &str {
        &self.id
    }

    fn dependencies(&self) -> &[String] {
        &[]
    }

    fn execute(&self, _ctx: &mut ExecutionContext) -> Result<StepResult> {
        let metrics = StepMetrics::new(self.id.clone());
        Ok(StepResult::new(Value::Null, metrics))
    }
}

/// A step with configurable CPU work.
struct CpuWorkStep {
    id: String,
    iterations: u64,
}

impl CpuWorkStep {
    fn new(id: &str, iterations: u64) -> Self {
        Self {
            id: id.to_string(),
            iterations,
        }
    }
}

impl Step for CpuWorkStep {
    fn id(&self) -> &str {
        &self.id
    }

    fn dependencies(&self) -> &[String] {
        &[]
    }

    fn execute(&self, _ctx: &mut ExecutionContext) -> Result<StepResult> {
        // Simulate CPU work
        let mut sum: u64 = 0;
        for i in 0..self.iterations {
            sum = sum.wrapping_add(i);
        }
        black_box(sum); // Prevent optimization

        let metrics = StepMetrics::new(self.id.clone());
        Ok(StepResult::new(Value::from(sum), metrics))
    }

    fn resource_hint(&self) -> ResourceHint {
        ResourceHint::HeavyCPU
    }
}

/// A step with a dependency.
struct DependentStep {
    id: String,
    dependencies: Vec<String>,
}

impl DependentStep {
    fn new(id: &str, dependencies: Vec<String>) -> Self {
        Self {
            id: id.to_string(),
            dependencies,
        }
    }
}

impl Step for DependentStep {
    fn id(&self) -> &str {
        &self.id
    }

    fn dependencies(&self) -> &[String] {
        &self.dependencies
    }

    fn execute(&self, _ctx: &mut ExecutionContext) -> Result<StepResult> {
        let metrics = StepMetrics::new(self.id.clone());
        Ok(StepResult::new(Value::Null, metrics))
    }
}

// ============================================================================
// Benchmarks
// ============================================================================

fn bench_sequential_overhead(c: &mut Criterion) {
    let mut group = c.benchmark_group("sequential_overhead");

    for num_steps in [1, 5, 10, 20, 50].iter() {
        group.throughput(Throughput::Elements(*num_steps as u64));
        group.bench_with_input(
            BenchmarkId::from_parameter(num_steps),
            num_steps,
            |b, &num_steps| {
                b.iter(|| {
                    let config = ExecutorConfig::default();
                    let mut executor = WorkflowExecutor::new(config);

                    for i in 0..num_steps {
                        executor.add_step(Box::new(MinimalStep::new(&format!("step_{}", i))));
                    }

                    executor.execute().unwrap()
                });
            },
        );
    }

    group.finish();
}

fn bench_parallel_speedup(c: &mut Criterion) {
    let mut group = c.benchmark_group("parallel_speedup");
    let iterations = 100_000; // Work per step

    for num_steps in [4, 8, 16].iter() {
        // Sequential baseline
        group.bench_with_input(
            BenchmarkId::new("sequential", num_steps),
            num_steps,
            |b, &num_steps| {
                b.iter(|| {
                    let config = ExecutorConfig::default();
                    let mut executor = WorkflowExecutor::new(config);

                    for i in 0..num_steps {
                        executor.add_step(Box::new(CpuWorkStep::new(
                            &format!("step_{}", i),
                            iterations,
                        )));
                    }

                    executor.execute().unwrap()
                });
            },
        );

        // Parallel with 4 threads
        group.bench_with_input(
            BenchmarkId::new("parallel_4", num_steps),
            num_steps,
            |b, &num_steps| {
                b.iter(|| {
                    let config = ExecutorConfig::builder().max_parallel_steps(4).build();
                    let mut executor = WorkflowExecutor::new(config);

                    for i in 0..num_steps {
                        executor.add_step(Box::new(CpuWorkStep::new(
                            &format!("step_{}", i),
                            iterations,
                        )));
                    }

                    executor.execute_parallel().unwrap()
                });
            },
        );
    }

    group.finish();
}

fn bench_cancellation_check(c: &mut Criterion) {
    let mut group = c.benchmark_group("cancellation");

    // Baseline: no cancellation
    group.bench_function("no_cancellation", |b| {
        b.iter(|| {
            let config = ExecutorConfig::default();
            let mut executor = WorkflowExecutor::new(config);

            for i in 0..20 {
                executor.add_step(Box::new(MinimalStep::new(&format!("step_{}", i))));
            }

            executor.execute().unwrap()
        });
    });

    // With cancellation token (not cancelled)
    group.bench_function("with_token_not_cancelled", |b| {
        b.iter(|| {
            let config = ExecutorConfig::default();
            let mut executor = WorkflowExecutor::new(config);

            for i in 0..20 {
                executor.add_step(Box::new(MinimalStep::new(&format!("step_{}", i))));
            }

            let token = CancellationToken::new();
            executor.execute_with_options(Some(token), None).unwrap()
        });
    });

    // Token check latency
    group.bench_function("token_check_latency", |b| {
        let token = CancellationToken::new();
        b.iter(|| {
            for _ in 0..1000 {
                black_box(token.is_cancelled());
            }
        });
    });

    group.finish();
}

fn bench_dag_operations(c: &mut Criterion) {
    let mut group = c.benchmark_group("dag_operations");

    // Linear DAG
    group.bench_function("linear_dag_50_steps", |b| {
        b.iter(|| {
            let config = ExecutorConfig::default();
            let mut executor = WorkflowExecutor::new(config);

            executor.add_step(Box::new(MinimalStep::new("step_0")));
            for i in 1..50 {
                executor.add_step(Box::new(DependentStep::new(
                    &format!("step_{}", i),
                    vec![format!("step_{}", i - 1)],
                )));
            }

            executor.execute().unwrap()
        });
    });

    // Wide DAG (many independent steps)
    group.bench_function("wide_dag_50_steps", |b| {
        b.iter(|| {
            let config = ExecutorConfig::builder().max_parallel_steps(8).build();
            let mut executor = WorkflowExecutor::new(config);

            for i in 0..50 {
                executor.add_step(Box::new(MinimalStep::new(&format!("step_{}", i))));
            }

            executor.execute_parallel().unwrap()
        });
    });

    // Diamond DAG
    group.bench_function("diamond_dag", |b| {
        b.iter(|| {
            let config = ExecutorConfig::builder().max_parallel_steps(4).build();
            let mut executor = WorkflowExecutor::new(config);

            // Root
            executor.add_step(Box::new(MinimalStep::new("root")));

            // Layer 1 (depends on root)
            for i in 0..4 {
                executor.add_step(Box::new(DependentStep::new(
                    &format!("l1_{}", i),
                    vec!["root".to_string()],
                )));
            }

            // Layer 2 (depends on all layer 1)
            executor.add_step(Box::new(DependentStep::new(
                "merge",
                (0..4).map(|i| format!("l1_{}", i)).collect(),
            )));

            executor.execute_parallel().unwrap()
        });
    });

    group.finish();
}

fn bench_step_execution_cost(c: &mut Criterion) {
    let mut group = c.benchmark_group("step_execution_cost");

    group.bench_function("minimal_step", |b| {
        let mut ctx = ExecutionContext::new();
        let step = MinimalStep::new("test");
        b.iter(|| step.execute(&mut ctx).unwrap());
    });

    group.bench_function("cpu_work_10k", |b| {
        let mut ctx = ExecutionContext::new();
        let step = CpuWorkStep::new("test", 10_000);
        b.iter(|| step.execute(&mut ctx).unwrap());
    });

    group.bench_function("cpu_work_100k", |b| {
        let mut ctx = ExecutionContext::new();
        let step = CpuWorkStep::new("test", 100_000);
        b.iter(|| step.execute(&mut ctx).unwrap());
    });

    group.finish();
}

fn bench_executor_construction(c: &mut Criterion) {
    let mut group = c.benchmark_group("executor_construction");

    group.bench_function("create_executor", |b| {
        b.iter(|| {
            let config = ExecutorConfig::default();
            black_box(WorkflowExecutor::new(config))
        });
    });

    group.bench_function("add_10_steps", |b| {
        b.iter(|| {
            let config = ExecutorConfig::default();
            let mut executor = WorkflowExecutor::new(config);

            for i in 0..10 {
                executor.add_step(Box::new(MinimalStep::new(&format!("step_{}", i))));
            }

            black_box(executor)
        });
    });

    group.bench_function("add_100_steps", |b| {
        b.iter(|| {
            let config = ExecutorConfig::default();
            let mut executor = WorkflowExecutor::new(config);

            for i in 0..100 {
                executor.add_step(Box::new(MinimalStep::new(&format!("step_{}", i))));
            }

            black_box(executor)
        });
    });

    group.finish();
}

fn bench_parallel_scaling(c: &mut Criterion) {
    let mut group = c.benchmark_group("parallel_scaling");
    group.measurement_time(Duration::from_secs(10));

    let num_steps = 32;
    let iterations = 50_000;

    for parallelism in [1, 2, 4, 8].iter() {
        group.bench_with_input(
            BenchmarkId::from_parameter(parallelism),
            parallelism,
            |b, &parallelism| {
                b.iter(|| {
                    let config = ExecutorConfig::builder()
                        .max_parallel_steps(parallelism)
                        .build();
                    let mut executor = WorkflowExecutor::new(config);

                    for i in 0..num_steps {
                        executor.add_step(Box::new(CpuWorkStep::new(
                            &format!("step_{}", i),
                            iterations,
                        )));
                    }

                    executor.execute_parallel().unwrap()
                });
            },
        );
    }

    group.finish();
}

fn bench_resource_hints(c: &mut Criterion) {
    let mut group = c.benchmark_group("resource_hints");

    let num_steps = 16;
    let iterations = 100_000;

    // With resource hints (HeavyCPU)
    group.bench_function("with_hints", |b| {
        b.iter(|| {
            let config = ExecutorConfig::builder().max_parallel_steps(4).build();
            let mut executor = WorkflowExecutor::new(config);

            for i in 0..num_steps {
                executor.add_step(Box::new(CpuWorkStep::new(
                    &format!("step_{}", i),
                    iterations,
                )));
            }

            executor.execute_parallel().unwrap()
        });
    });

    // Without resource hints (MinimalStep)
    group.bench_function("without_hints", |b| {
        b.iter(|| {
            let config = ExecutorConfig::builder().max_parallel_steps(4).build();
            let mut executor = WorkflowExecutor::new(config);

            for i in 0..num_steps {
                executor.add_step(Box::new(MinimalStep::new(&format!("step_{}", i))));
            }

            executor.execute_parallel().unwrap()
        });
    });

    group.finish();
}

criterion_group!(
    benches,
    bench_sequential_overhead,
    bench_parallel_speedup,
    bench_cancellation_check,
    bench_dag_operations,
    bench_step_execution_cost,
    bench_executor_construction,
    bench_parallel_scaling,
    bench_resource_hints,
);
criterion_main!(benches);
