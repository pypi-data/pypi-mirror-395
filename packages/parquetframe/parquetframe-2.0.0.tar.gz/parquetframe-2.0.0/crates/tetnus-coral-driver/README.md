# Tetnus Coral Driver

Rust FFI bindings for Google Coral Edge TPU (`libedgetpu.so`).

## Features

- **Mock Mode (Default)**: Development without Coral hardware
- **Hardware Mode**: Real Edge TPU inference when `coral-hardware` feature is enabled

## Usage

### Mock Mode (Development)
```rust
use tetnus_coral_driver::CoralContext;

let model_data = std::fs::read("model.tflite")?;
let ctx = CoralContext::new(&model_data)?;

let input = vec![0u8; 100];
let mut output = vec![0u8; 100];
ctx.invoke(&input, &mut output)?;
```

### Hardware Mode (Production)
Enable the `coral-hardware` feature in `Cargo.toml`:
```toml
[dependencies]
tetnus-coral-driver = { version = "1.0", features = ["coral-hardware"] }
```

## Requirements (Hardware Mode)

1. **Google Coral Edge TPU** device
2. **libedgetpu.so** installed:
   ```bash
   # Install Edge TPU runtime
   echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list
   curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
   sudo apt-get update
   sudo apt-get install libedgetpu1-std
   ```

3. **Compiled TFLite model** for Edge TPU:
   ```bash
   edgetpu_compiler model.tflite
   ```

## Testing

```bash
# Test mock implementation (no hardware needed)
cargo test

# Test with hardware (requires Coral device)
cargo test --features coral-hardware
```

## Architecture

```
Mock Mode:     CoralContext (mock) → Dummy inference
              ↓
Hardware Mode: CoralContext (FFI) → libedgetpu.so → Edge TPU
```

## Safety

The FFI bindings use `unsafe` Rust to interface with C code. The `CoralContext` wrapper ensures:
- Proper resource cleanup via `Drop`
- No use-after-free via ownership
- Thread safety via `Send` marker

## Limitations

- Currently supports single-threaded inference only
- Input/output tensors must be pre-allocated
- Quantization must be performed before compilation
