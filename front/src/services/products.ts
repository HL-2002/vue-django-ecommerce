import type { Category, Product, SimplifiedProduct } from "@/types/types";

export const API_URL = "http://localhost:8000";


export  async function getCategories(): Promise<{
id: number;
name: string;
}[]> {
  const response = await fetch(`${API_URL}/API/category/?format=json`);
  return response.json();
}

export async function createCategory(category: {name: string}): Promise<Category> {
const response = await fetch(`${API_URL}/API/category/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(category),
  });
  return response.json();
}

export async function createTag(tag:{name:string}): Promise<{id:number,name:string}> {

 const response = await fetch(`${API_URL}/API/tag/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(tag),
  });
  return response.json()

}

export async function getTags(): Promise<Array<{id:number,name:string}>>{

  const response = await fetch(`${API_URL}/API/tag/?format=json`);
  return response.json();

}






export async function getProducts() : Promise<Product[]> {
  const response = await fetch(`${API_URL}/API/product/?format=json`);
  return response.json();
}


export  async function createProduct(product ): Promise<void> {
  //por ahora esta logica no existe falta esa parte del back
  console.log("enviando al back",product);

}
