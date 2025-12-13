use crate::sparse::SparseTensor;
use tetnus_core::Tensor;
use pf_graph_core::CsrGraph;

pub struct Graph {
    pub x: Tensor,           // Node features [N, F]
    pub edge_index: SparseTensor, // Adjacency [N, N]
}

impl Graph {
    pub fn new(x: Tensor, edge_index: SparseTensor) -> Self {
        Self { x, edge_index }
    }

    pub fn from_parquetframe(_pf_graph: &CsrGraph) -> Self {
        // 1. Convert Vertices DataFrame to Tensor X
        // This assumes the vertices dataframe has numerical columns that we want to use as features.
        // In a real scenario, we'd select specific columns.
        // For this MVP, we'll assume a simple conversion or placeholder.

        // let vertices_df = &pf_graph.vertices;
        // let x = vertices_df.to_tensor(); // Assuming DataFrame has this extension or we implement it here.

        // Placeholder: Create a dummy tensor for X
        let x = Tensor::zeros(vec![10, 5]).expect("Failed to create tensor"); // 10 nodes, 5 features

        // 2. Convert Edges to SparseTensor
        // pf_graph.edges is typically an EdgeList (src, dst)
        // We need to extract src and dst columns and create a SparseTensor.

        // Placeholder: Create a dummy sparse tensor
        let indices = Tensor::zeros(vec![2, 20]).expect("Failed to create indices"); // 20 edges
        let values = Tensor::ones(vec![20]).expect("Failed to create values");
        let edge_index = SparseTensor::new(indices, values, vec![10, 10]);

        Self::new(x, edge_index)
    }
}
