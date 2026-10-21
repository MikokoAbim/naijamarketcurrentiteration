export const getItemById = async (item_id) => {
    const res = await fetch(`http://127.0.0.1:8000/marketplace/item/${item_id}`)
    return res.json();
}