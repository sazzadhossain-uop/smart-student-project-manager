export class ItemService {
    fetchAllItems(): Promise<Item[]> {
        // Logic to fetch all items from the data source
    }

    fetchItemById(id: string): Promise<Item | null> {
        // Logic to fetch a single item by its ID from the data source
    }
}