fn main() {
    #[cfg(target_os = "macos")]
    {
        // Allow unresolved Python symbols to be dynamically looked up at runtime.
        println!("cargo:rustc-link-arg=-undefined");
        println!("cargo:rustc-link-arg=dynamic_lookup");
    }
}
