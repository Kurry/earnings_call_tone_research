# Earnings Call Tone Research - GitHub Pages Documentation

This directory contains the GitHub Pages site for the earnings call tone dispersion research project.

## Site Structure

- `index.md` - Homepage with executive summary
- `methodology.md` - Detailed methodology and factor construction
- `results.md` - Performance analysis and visualizations
- `technical.md` - Technical implementation documentation
- `assets/` - CSS, JavaScript, and image assets
- `_config.yml` - Jekyll configuration

## Local Development

To run the site locally:

```bash
# Install Ruby and Bundler (if not already installed)
# On macOS: brew install ruby
# On Ubuntu: sudo apt-get install ruby-full

# Navigate to docs directory
cd docs/

# Install dependencies
bundle install

# Serve the site locally
bundle exec jekyll serve

# Open http://localhost:4000 in your browser
```

## Deployment

The site is automatically deployed to GitHub Pages via GitHub Actions when changes are pushed to the `docs/` directory on the main branch.

### Manual Deployment

If needed, you can manually trigger deployment:
1. Go to the GitHub repository
2. Click on the "Actions" tab
3. Select "Deploy GitHub Pages" workflow
4. Click "Run workflow"

## Adding Content

### New Pages
1. Create a new `.md` file in the `docs/` directory
2. Add appropriate front matter:
   ```yaml
   ---
   layout: default
   title: "Page Title"
   permalink: /page-url/
   ---
   ```
3. Add the page to navigation in `_config.yml`

### Images
1. Add images to `docs/assets/images/`
2. Reference in markdown: `![Alt text](assets/images/filename.png)`

### Interactive Elements
- JavaScript interactions are in `assets/js/interactive.js`
- CSS styling is in `assets/css/main.scss`
- Use HTML elements with appropriate classes for styling

## Site Features

### Interactive Elements
- Animated performance metrics
- Interactive quintile performance chart
- Sortable tables
- Hover effects and tooltips

### Responsive Design
- Mobile-friendly layout
- Responsive tables and images
- Optimized for various screen sizes

### Performance
- Optimized images
- Minimal JavaScript
- Fast loading times

## Customization

### Colors and Styling
Edit `assets/css/main.scss` to customize:
- Color scheme
- Typography
- Layout spacing
- Component styling

### Interactive Features
Edit `assets/js/interactive.js` to:
- Add new visualizations
- Modify table behavior
- Create new interactive elements

## Content Guidelines

### Writing Style
- Use clear, professional language
- Include technical details but keep accessible
- Add interpretations for all metrics
- Use consistent terminology

### Data Presentation
- Always include units (bps, %, etc.)
- Use color coding for positive/negative values
- Provide context and interpretation
- Include data sources and dates

### Images and Charts
- Use high-resolution images (300 DPI)
- Include alt text for accessibility
- Optimize file sizes
- Use consistent styling

## Troubleshooting

### Common Issues

**Bundle install fails:**
```bash
# Update bundler
gem update bundler
bundle install
```

**Jekyll serve fails:**
```bash
# Clear cache and rebuild
bundle exec jekyll clean
bundle exec jekyll serve
```

**Pages not updating:**
- Check GitHub Actions for build errors
- Verify file paths and front matter
- Clear browser cache

### Getting Help
- Check Jekyll documentation: https://jekyllrb.com/docs/
- GitHub Pages documentation: https://docs.github.com/en/pages
- File issues in the project repository

## Site Analytics

The site includes:
- SEO optimization via jekyll-seo-tag
- Sitemap generation via jekyll-sitemap
- RSS feed via jekyll-feed
- (Optional) Google Analytics integration

## License

This documentation site is part of the earnings call tone research project. See the main repository for licensing information.