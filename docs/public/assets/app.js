document.addEventListener('DOMContentLoaded', async () => {
    const container = document.getElementById('brief-items');
    try {
        const response = await fetch('data/brief_today.json');
        const data = await response.json();
        container.textContent = `Loaded ${data.items?.length || 0} items`;
    } catch (error) {
        container.textContent = 'No brief available yet. Run the pipeline to generate content.';
    }
});
