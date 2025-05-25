# GitHub Pages Setup Guide

This guide explains how to set up and deploy the earnings call tone research documentation site using GitHub Pages.

## Quick Setup

1. **Enable GitHub Pages**:
   - Go to your repository on GitHub
   - Click **Settings** → **Pages**
   - Under **Source**, select **GitHub Actions**
   - The site will automatically deploy from the `docs/` folder

2. **Repository URL**:
   - The URL is already configured for `https://kurry.github.io/earnings_call_tone_research`
   - No changes needed unless you fork to a different account

3. **Push Changes**:
   ```bash
   git add docs/
   git commit -m "Add GitHub Pages documentation site"
   git push origin main
   ```

4. **Access Your Site**:
   - Visit `https://kurry.github.io/earnings_call_tone_research`
   - The site will be available within a few minutes

## Site Structure

```
docs/
├── _config.yml              # Jekyll configuration
├── index.md                 # Homepage
├── methodology.md           # Factor construction details
├── results.md              # Performance analysis
├── technical.md            # Implementation docs
├── Gemfile                 # Ruby dependencies
├── assets/
│   ├── css/main.scss       # Custom styling
│   ├── js/interactive.js   # JavaScript interactions
│   ├── images/             # Generated charts and plots
│   └── data/              # Exported metrics (JSON)
└── README.md              # Documentation setup guide
```

## Features Included

### 📊 **Performance Dashboard**
- Interactive metrics display
- Quintile performance visualization
- Sortable performance tables
- Real-time data updates

### 📈 **Visualizations**
- Factor performance summary charts
- Quintile analysis with interactive elements
- Methodology flowchart
- Turnover and drawdown analysis

### 🎨 **Professional Design**
- Responsive mobile-friendly layout
- Modern CSS with animations
- Professional color scheme
- Accessible design principles

### ⚡ **Interactive Elements**
- Clickable quintile charts with detailed popups
- Sortable data tables
- Smooth scrolling navigation
- Hover effects and animations

## Customization Options

### 1. **Update Content**
- Edit `.md` files in the `docs/` directory
- Add new sections or pages as needed
- Include your specific research findings

### 2. **Modify Styling**
- Edit `docs/assets/css/main.scss` for visual changes
- Customize colors, fonts, and layout
- Add company branding if needed

### 3. **Add Visualizations**
- Run `python generate_docs_assets.py` to create new charts
- Add custom plots to `docs/assets/images/`
- Update pages to reference new visualizations

### 4. **Interactive Features**
- Modify `docs/assets/js/interactive.js` for new interactions
- Add data-driven visualizations
- Integrate with external APIs if needed

## Advanced Setup

### Custom Domain (Optional)
1. Purchase a domain name
2. Add a `CNAME` file to `docs/` with your domain
3. Configure DNS settings with your domain provider
4. Update `url` in `_config.yml`

### Analytics Integration
1. Get Google Analytics tracking ID
2. Uncomment and update `google_analytics` in `_config.yml`
3. Add other analytics services as needed

### SEO Optimization
- Update meta descriptions in each page's front matter
- Add relevant keywords
- Optimize image alt tags
- Submit sitemap to search engines

## Updating Content

### 1. **Regular Updates**
```bash
# Update research results
python run_backtest.py           # Generate latest results
python generate_docs_assets.py   # Update visualizations
git add docs/assets/images/      # Add new charts
git commit -m "Update research results for [DATE]"
git push origin main
```

### 2. **Content Maintenance**
- Review and update performance metrics quarterly
- Add new research findings as they become available  
- Update methodology if processes change
- Refresh visualizations with latest data

### 3. **Version Control**
- Tag major releases: `git tag v1.0`
- Maintain changelog in documentation
- Track performance changes over time

## Troubleshooting

### Site Not Loading
1. Check GitHub Actions for build errors
2. Verify `_config.yml` syntax
3. Ensure all file paths are correct
4. Check that GitHub Pages is enabled in settings

### Styling Issues
1. Clear browser cache
2. Check CSS syntax in `main.scss`
3. Verify Jekyll build logs
4. Test locally with `bundle exec jekyll serve`

### JavaScript Not Working
1. Check browser console for errors
2. Verify file paths in script includes
3. Test interactive elements locally
4. Ensure jQuery/dependencies are loaded

### Performance Issues
1. Optimize image sizes (use tools like ImageOptim)
2. Minimize CSS and JavaScript
3. Enable compression in GitHub Pages
4. Consider using a CDN for assets

## Best Practices

### 📝 **Content**
- Keep technical explanations accessible
- Include clear interpretations of all metrics
- Use consistent terminology throughout
- Provide context for all findings

### 🎨 **Design**
- Maintain consistent visual hierarchy
- Use appropriate color coding (green=positive, red=negative)
- Ensure mobile responsiveness
- Optimize for fast loading

### 📊 **Data Presentation**
- Always include units (bps, %, etc.)
- Provide hover tooltips for complex charts
- Use interactive elements judiciously
- Include data sources and update dates

### 🔄 **Maintenance**
- Set up automated data updates if possible
- Monitor site performance and user feedback
- Keep dependencies updated
- Backup important data and configurations

## Next Steps

1. **Customize for Your Needs**:
   - Update content with your specific research findings
   - Modify styling to match your organization's branding
   - Add any additional analysis or visualizations

2. **Share and Collaborate**:
   - Share the site URL with stakeholders
   - Gather feedback and iterate on design
   - Consider adding collaboration features

3. **Expand Functionality**:
   - Add more interactive visualizations
   - Integrate with data APIs for real-time updates
   - Create downloadable reports
   - Add research comparison tools

---

## Support

For technical issues:
- Check the Jekyll documentation: https://jekyllrb.com/
- Review GitHub Pages documentation: https://docs.github.com/en/pages
- File issues in the project repository

For customization help:
- Review the code documentation in `technical.md`
- Examine the existing CSS and JavaScript files
- Consider hiring a web developer for major modifications

**Your professional research documentation site is now ready to showcase your earnings call tone dispersion analysis!** 🚀