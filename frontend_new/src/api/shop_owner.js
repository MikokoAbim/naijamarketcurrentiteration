export const getShopOwnerById = async (shop_owner_id) => {
    const res = await fetch(`http://127.0.0.1:8000/naija_market/shop_owner/${shop_owner_id}`)
    return res.json();
}

