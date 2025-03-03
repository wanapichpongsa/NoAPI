use dioxus::prelude::*;

#[component]
pub fn Home() -> Element {
    rsx! {
        div {
            h1 { "Hello, World!" }
        }
    }
}

// What I want homepage to look like...
/*
1. Middle menu
2. Navbar on top
3. Chatbox with conversation, datastructure editing, and graph visualization. Else... put all in the same page. Wait no. Better to have only 1 ds or graph per query.
*/