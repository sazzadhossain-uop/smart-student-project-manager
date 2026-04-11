export interface Item {
    id: number;
    name: string;
    description: string;
    price: number;
}

export interface ApiResponse<T> {
    success: boolean;
    data: T;
    message?: string;
}