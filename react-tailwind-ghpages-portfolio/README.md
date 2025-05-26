# React Tailwind GitHub Pages Portfolio

This is a simple portfolio website built using React, Vite, and Tailwind CSS, designed for easy deployment to GitHub Pages.

## Project Structure

-   **`/.github/workflows/deploy.yml`**: GitHub Actions workflow for automated deployment.
-   **`/public`**: Static assets.
-   **`/src`**: Source files.
    -   **`/components`**: Reusable React components.
    -   **`App.jsx`**: Main application component orchestrating the page layout.
    -   **`index.css`**: Tailwind CSS directives and any global styles.
    -   **`main.jsx`**: Entry point of the React application.
-   **`index.html`**: Main HTML file for Vite.
-   **`package.json`**: Project dependencies and scripts.
-   **`tailwind.config.js`**: Tailwind CSS configuration.
-   **`vite.config.js`**: Vite configuration, including the `base` path for GitHub Pages.

## Local Development

1.  **Clone the repository (if you haven't already):**
    ```bash
    git clone https://github.com/yourusername/react-tailwind-ghpages-portfolio.git
    cd react-tailwind-ghpages-portfolio
    ```
    *(Replace `yourusername` with your actual GitHub username if you've pushed this to your own repo).*

2.  **Install dependencies:**
    ```bash
    npm install
    ```

3.  **Run the development server:**
    ```bash
    npm run dev
    ```
    This will start the Vite development server, typically at `http://localhost:5173`.

## Building the Project

To create a production build in the `dist` folder:
```bash
npm run build
```

## Deployment to GitHub Pages

### Automated Deployment (Recommended)

This project is configured for automated deployment using GitHub Actions.
1.  Push your changes to the `main` branch of your GitHub repository.
2.  The GitHub Action defined in `.github/workflows/deploy.yml` will automatically build the project and deploy it to the `gh-pages` branch.
3.  Your site will be available at `https://yourusername.github.io/react-tailwind-ghpages-portfolio/` (replace `yourusername` with your GitHub username).

### Manual Deployment (Alternative)

If you need to deploy manually:
1.  Ensure your `vite.config.js` has the correct `base` path (`/react-tailwind-ghpages-portfolio/`).
2.  Ensure your `package.json` has the `homepage` field correctly set.
3.  Run the deployment script:
    ```bash
    npm run deploy
    ```
    This command first runs `npm run build` (predeploy script) and then uses `gh-pages` to push the contents of the `dist` folder to the `gh-pages` branch.

## Customization

-   **Content:** Modify the JSX files in `src/components/` to change the text, images, and project details.
-   **Styling:** Adjust Tailwind CSS classes within the components. Modify `tailwind.config.js` for broader theme changes (colors, fonts, etc.).
-   **Repository Name:** If your GitHub repository has a different name, update:
    -   The `base` path in `vite.config.js`.
    -   The `homepage` URL in `package.json`.
    -   The deployment URL in this README.
