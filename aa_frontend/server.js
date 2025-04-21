const express = require('express');
const path = require('path');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.json());

app.use('/home', express.static(path.join(__dirname, 'home')));

// Render dynamic form from API
app.get('/form/:id', async (req, res) => {
  const userId = req.params.id;

  try {
    const response = await fetch(`http://127.0.0.1:8000/api/forms/${userId}/`);
    const form = await response.json();

    const formFieldsHtml = form.fields.map(field => `
      <label>${field.label}:</label>
      <input 
        type="${field.type}" 
        name="${field.label}" 
        placeholder="${field.placeholder || ''}" 
        ${field.required ? 'required' : ''}
      /><br/>
    `).join('');

    const html = `
      <html>
      <body>
        <h2>${form.title}</h2>
        <form method="POST" action="/submit/${form.id}">
          ${formFieldsHtml}
          <button type="submit">Submit</button>
        </form>
      </body>
      </html>
    `;
    res.send(html);

  } catch (error) {
    res.status(500).send('Error fetching form data');
  }
});

// Handle form submission
app.post('/submit/:formId', async (req, res) => {
    const formId = req.params.formId;
    const submittedData = req.body;
  
    try {
      // Send the form data to an external API using fetch
      const apiResponse = await fetch(`http://127.0.0.1:8000/api/forms/${formId}/post-response/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(submittedData),
      });
  
      if (apiResponse.ok) {
        const apiResponseData = await apiResponse.json();
        res.json({
          message: `Form ${formId} submitted successfully to external API`,
          data: submittedData,
          apiResponse: apiResponseData
        });
      } else {
        const errorData = await apiResponse.json();
        res.status(500).json({
          message: `Form ${formId} submission failed on external API`,
          error: errorData
        });
      }
    } catch (error) {
      // Handle error from external API request
      res.status(500).json({
        message: `Error submitting form ${formId} to external API`,
        error: error.message
      });
    }
  });
  

app.listen(3000, () => {
  console.log('Server running on http://localhost:3000');
});
