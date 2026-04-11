interface Item {
    id: string;
    [key: string]: any;
}

export class ItemService {
    fetchAllItems(): Promise<Item[]> {
        // Logic to fetch all items from the data source
        return Promise.resolve([]);
    }

    fetchItemById(id: string): Promise<Item | null> {
        // Logic to fetch a single item by its ID from the data source
        return Promise.resolve(null);
    }
}