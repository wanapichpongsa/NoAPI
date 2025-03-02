use crate::components::{Echo, Hero};
use dioxus::prelude::*;

#[component]
pub fn Home() -> Element {
    rsx! {
        Echo {}
    }
}
