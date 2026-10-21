export const getShopById = async (shop_id) => {
    const res = await fetch(`http://127.0.0.1:8000/marketplace/shops/${shop_id}`)
    return res.json();
}