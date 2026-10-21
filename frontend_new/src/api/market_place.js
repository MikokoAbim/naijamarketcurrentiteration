export const getMarketplace = async () => {
    const res = await fetch("http://127.0.0.1:8000/marketplace/");
    return res.json();
};

export const getShopByName = async (shop_name) => {
    const res = await fetch(`http://127.0.0.1:8000/marketplace/shops/by-name?name=${shop_name}`);
    return res.json();
};