use crate::module::Module;
use crate::Result;
use tetnus_core::Tensor;

pub struct Sequential {
    modules: Vec<Box<dyn Module>>,
}

impl Sequential {
    pub fn new() -> Self {
        Self {
            modules: Vec::new(),
        }
    }

    pub fn add(&mut self, module: Box<dyn Module>) {
        self.modules.push(module);
    }
}

impl Module for Sequential {
    fn forward(&self, input: &Tensor) -> Result<Tensor> {
        let mut x = input.clone();
        for module in &self.modules {
            x = module.forward(&x)?;
        }
        Ok(x)
    }

    fn parameters(&self) -> Vec<Tensor> {
        self.modules.iter().flat_map(|m| m.parameters()).collect()
    }
}
