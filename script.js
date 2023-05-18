window.addEventListener('DOMContentLoaded', () => {
    // Fetch data from data.json
    fetch('data.json')
      .then(response => response.json())
      .then(data => {
        // Set customer information
        document.getElementById('customer-name').textContent = `Customer Name: ${data.customerName}`;
        document.getElementById('job-address').textContent = `Job Address: ${data.jobAddress}`;
  
        // Set job description
        document.getElementById('job-description').textContent = `Job Description: ${data.jobDescription}`;
  
        // Set granite prices
        const granitePricesDiv = document.getElementById('granite-prices');
        data.granitePrices.forEach(price => {
          const div = document.createElement('div');
          div.textContent = `${price.tierName}: $${price.price} - Colors: ${price.colors.join(', ')}`;
          granitePricesDiv.appendChild(div);
        });
  
        // Set quartz prices
        const quartzPricesDiv = document.getElementById('quartz-prices');
        data.quartzPrices.forEach(price => {
          const div = document.createElement('div');
          div.textContent = `${price.tierName}: $${price.price} - Colors: ${price.colors.join(', ')}`;
          quartzPricesDiv.appendChild(div);
        });
  
        // Set edge options
        const edgeOptionsDiv = document.getElementById('edge-options');
        data.edgeOptions.forEach(option => {
          const div = document.createElement('div');
          div.textContent = `${option.optionName}: $${option.price}`;
          edgeOptionsDiv.appendChild(div);
        });
      })
      .catch(error => console.log(error));
  });
  