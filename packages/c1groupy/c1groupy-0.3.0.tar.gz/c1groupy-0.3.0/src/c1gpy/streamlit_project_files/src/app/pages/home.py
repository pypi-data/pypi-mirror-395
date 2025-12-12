import streamlit as st


st.title("Welcome to {project_name}")
st.write("This is a multi-page Streamlit application using st.navigation().")

st.markdown("""
## Navigation
Use the sidebar to navigate between pages organized in sections.

## Getting Started
- Edit `src/app/App.py` to customize the navigation structure
- Add new pages in the `src/app/pages/` directory
- Update the `pages` dictionary in `App.py` to include your new pages

## Page Structure
Pages are organized into sections:
- **Main**: Your primary application pages
- **Info**: Documentation and support pages

## Adding New Pages
1. Create a new Python file in `src/app/pages/`
2. Add it to the `pages` dictionary in `App.py`:
```python
st.Page("pages/your_page.py", title="Your Page", icon="🎯")
```
""")
