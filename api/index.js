const express = require('express');
const app = express();
const port = 3000;

const exemploRoutes = require('./routes/exemploRoutes');
app.use(express.json());
app.use('/api/exemplo', exemploRoutes);

// Servir front-end
app.use(express.static('public'));

app.listen(port, () => {
  console.log(`Servidor rodando em http://localhost:${port}`);
});
