use std::collections::{HashMap, VecDeque};
use crate::schema::{WorkflowDefinition, Step};
use crate::executors::{ExecutionContext, StepExecutor, ExecutionError};

pub struct WorkflowRunner {
    definition: WorkflowDefinition,
    executors: HashMap<String, Box<dyn StepExecutor>>,
}

impl WorkflowRunner {
    pub fn new(definition: WorkflowDefinition) -> Self {
        Self {
            definition,
            executors: HashMap::new(),
        }
    }

    pub fn register_executor(&mut self, type_name: &str, executor: Box<dyn StepExecutor>) {
        self.executors.insert(type_name.to_string(), executor);
    }

    pub async fn run(&self) -> Result<(), ExecutionError> {
        let mut ctx = ExecutionContext::new();

        // 1. Build DAG and Topological Sort
        let sorted_steps = self.topological_sort()?;

        // 2. Execute steps sequentially for MVP (Parallelism later)
        for step in sorted_steps {
            println!("Running step: {}", step.name);

            let executor = self.executors.get(&step.step_type)
                .ok_or_else(|| ExecutionError::StepFailed(format!("Unknown step type: {}", step.step_type)))?;

            // Resolve inputs
            let mut input_dfs = Vec::new();
            if let Some(input_name) = &step.input {
                if let Some(df) = ctx.get_handle(input_name) {
                    input_dfs.push(df);
                } else {
                    return Err(ExecutionError::StepFailed(format!("Input handle not found: {}", input_name)));
                }
            }
            if let Some(inputs) = &step.inputs {
                for input_name in inputs {
                    if let Some(df) = ctx.get_handle(input_name) {
                        input_dfs.push(df);
                    } else {
                        return Err(ExecutionError::StepFailed(format!("Input handle not found: {}", input_name)));
                    }
                }
            }

            // Execute
            let result_df = executor.execute(&step.params, input_dfs, &ctx).await?;

            // Register output
            if let Some(df) = result_df {
                if let Some(output_name) = &step.output {
                    ctx.register_handle(output_name, df.clone());
                    // Also register with SessionContext for SQL
                    ctx.session_ctx.register_table(output_name, (*df).clone().into_view())?;
                }
            }
        }

        Ok(())
    }

    fn topological_sort(&self) -> Result<Vec<&Step>, ExecutionError> {
        let mut adj: HashMap<&String, Vec<&String>> = HashMap::new();
        let mut in_degree: HashMap<&String, usize> = HashMap::new();
        let step_map: HashMap<&String, &Step> = self.definition.steps.iter().map(|s| (&s.name, s)).collect();

        for step in &self.definition.steps {
            in_degree.entry(&step.name).or_insert(0);

            // Dependencies from 'depends_on'
            for dep in &step.depends_on {
                adj.entry(dep).or_default().push(&step.name);
                *in_degree.entry(&step.name).or_insert(0) += 1;
            }

            // Implicit dependencies from inputs
            if let Some(input) = &step.input {
                // Find step that outputs this
                if let Some(producer) = self.find_producer(input) {
                    adj.entry(&producer.name).or_default().push(&step.name);
                    *in_degree.entry(&step.name).or_insert(0) += 1;
                }
            }
            if let Some(inputs) = &step.inputs {
                for input in inputs {
                    if let Some(producer) = self.find_producer(input) {
                        adj.entry(&producer.name).or_default().push(&step.name);
                        *in_degree.entry(&step.name).or_insert(0) += 1;
                    }
                }
            }
        }

        let mut queue = VecDeque::new();
        for (name, &degree) in &in_degree {
            if degree == 0 {
                queue.push_back(*name);
            }
        }

        let mut sorted = Vec::new();
        while let Some(name) = queue.pop_front() {
            sorted.push(step_map[name]);

            if let Some(neighbors) = adj.get(name) {
                for neighbor in neighbors {
                    let degree = in_degree.get_mut(neighbor).unwrap();
                    *degree -= 1;
                    if *degree == 0 {
                        queue.push_back(neighbor);
                    }
                }
            }
        }

        if sorted.len() != self.definition.steps.len() {
            return Err(ExecutionError::StepFailed("Cycle detected or missing dependency".to_string()));
        }

        Ok(sorted)
    }

    fn find_producer(&self, handle: &str) -> Option<&Step> {
        for step in &self.definition.steps {
            if let Some(out) = &step.output {
                if out == handle { return Some(step); }
            }
            if let Some(outs) = &step.outputs {
                if outs.contains(&handle.to_string()) { return Some(step); }
            }
        }
        None
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::schema::{WorkflowDefinition, Step, WorkflowConfig};

    fn create_step(name: &str, depends_on: Vec<&str>, input: Option<&str>, output: Option<&str>) -> Step {
        Step {
            name: name.to_string(),
            step_type: "test".to_string(),
            depends_on: depends_on.iter().map(|s| s.to_string()).collect(),
            input: input.map(|s| s.to_string()),
            inputs: None,
            output: output.map(|s| s.to_string()),
            outputs: None,
            params: HashMap::new(),
            resource_hint: None,
        }
    }

    #[test]
    fn test_topological_sort_linear() {
        let steps = vec![
            create_step("A", vec![], None, Some("a_out")),
            create_step("B", vec!["A"], Some("a_out"), Some("b_out")),
            create_step("C", vec!["B"], Some("b_out"), None),
        ];
        let def = WorkflowDefinition {
            version: "1.0".to_string(),
            config: WorkflowConfig::default(),
            steps
        };
        let runner = WorkflowRunner::new(def);
        let sorted = runner.topological_sort().unwrap();

        assert_eq!(sorted.len(), 3);
        assert_eq!(sorted[0].name, "A");
        assert_eq!(sorted[1].name, "B");
        assert_eq!(sorted[2].name, "C");
    }

    #[test]
    fn test_topological_sort_diamond() {
        // A -> B, A -> C, B -> D, C -> D
        let steps = vec![
            create_step("A", vec![], None, Some("a_out")),
            create_step("B", vec![], Some("a_out"), Some("b_out")), // Implicit dep on A via input
            create_step("C", vec!["A"], None, Some("c_out")),       // Explicit dep on A
            create_step("D", vec!["B", "C"], None, None),           // Explicit dep on B, C
        ];
        let def = WorkflowDefinition {
            version: "1.0".to_string(),
            config: WorkflowConfig::default(),
            steps
        };
        let runner = WorkflowRunner::new(def);
        let sorted = runner.topological_sort().unwrap();

        assert_eq!(sorted.len(), 4);
        assert_eq!(sorted[0].name, "A");
        // B and C can be in any order, but must be after A and before D
        let b_idx = sorted.iter().position(|s| s.name == "B").unwrap();
        let c_idx = sorted.iter().position(|s| s.name == "C").unwrap();
        let d_idx = sorted.iter().position(|s| s.name == "D").unwrap();

        assert!(b_idx > 0);
        assert!(c_idx > 0);
        assert!(d_idx > b_idx);
        assert!(d_idx > c_idx);
    }

    #[test]
    fn test_cycle_detection() {
        // A -> B -> A
        let steps = vec![
            create_step("A", vec!["B"], None, None),
            create_step("B", vec!["A"], None, None),
        ];
        let def = WorkflowDefinition {
            version: "1.0".to_string(),
            config: WorkflowConfig::default(),
            steps
        };
        let runner = WorkflowRunner::new(def);
        let result = runner.topological_sort();

        assert!(result.is_err());
    }

    #[test]
    fn test_missing_dependency() {
        // A -> B (B missing)
        let steps = vec![
            create_step("A", vec!["B"], None, None),
        ];
        let def = WorkflowDefinition {
            version: "1.0".to_string(),
            config: WorkflowConfig::default(),
            steps
        };
        let runner = WorkflowRunner::new(def);
        let result = runner.topological_sort();

        assert!(result.is_err());
    }
}
