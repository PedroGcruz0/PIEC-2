const express = require('express');
const cors = require('cors');
const path = require('path');

const app = express();
const porta = 3000;

app.use(cors());
app.use(express.json());

const rotaLogin = require('./routes/router');
app.use('/api/login', rotaLogin);

app.use(express.static(path.join(__dirname, '../public')));

app.listen(porta, () => {
  console.log(`Servidor rodando em http://localhost:${porta}`);
});
