import express from 'express';
import { IndexController } from './controllers/index';

const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());

const indexController = new IndexController();

app.get('/items', indexController.getAllItems.bind(indexController));
app.get('/items/:id', indexController.getItemById.bind(indexController));

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});