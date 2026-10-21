import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { getShopOwnerById } from '../api/shop_owner';
import AgentChat from "../components/AgentChat";

import '../styles/pages/Home.css';
import '../styles/pages/Shop_Owner.css';

export default function ShopOwnerProductAdd(){
    const navigate = useNavigate();
    const { shopOwnerId } = useParams();

    const [shop_owner, setShopOwner] = useState(null);
    const [form, setForm] = useState({
        name: "",
        description: "",
        price: "",
        image: "",
    });

    const [item, setItem] = useState(null);

    useEffect(() => {
        getShopOwnerById(shopOwnerId).then(data => setShopOwner(data));
    }, [shopOwnerId]);

    // how does this work
    const handleChange = (e) => {
        const { name, value } = e.target;
        // prev contains the previous state
        // we copy all old values with ...prev
        // then overwrite only the field that changed
        setForm(prev => ({ ...prev, [name]: value }));
    };
    //

    const handleSubmit = async () => {
        // placeholder — replace with real API call
        const response = await fetch("http://127.0.0.1:8000/naija_market/shop_owner/product_add", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                ...form,
                shop_id: shop_owner.shop.id
            })
        });
        const data = await response.json();
        
        if(data){
            const updateShopOwner = await getShopOwnerById(shopOwnerId)
            setShopOwner(updateShopOwner);
        }
    };

    if (!shop_owner) return <div>Loading...</div>;

    return(
        <div className="page">
            <aside className="sidebar">
                <div className="sidebar-logo">Logo</div>
                <div className="sidebar-item active" data-agent="nav-home" onClick={() => navigate("/")}>Home</div>
                <div className="sidebar-item" data-agent="nav-cart">Cart</div>
                <div className="sidebar-bottom" data-agent="nav-signin">Sign in</div>
            </aside>

            <div className="shopowner_content">
                <main className="shopowner_main">

                    <div className="shopowner_greeting">
                        Hi <span>{shop_owner.name}</span> — add a product to <span>{shop_owner.shop.name}</span>
                    </div>

                    <div className="shopowner_card">

                        <div className="shopowner_breadcrumb">🏷️ › Add product</div>

                        {/* TITLE */}
                        <div className="shopowner_field">
                            <label className="shopowner_label">Title</label>
                            <input
                                className="shopowner_input"
                                data-agent="shopowner-product-title-input"
                                name="name"
                                type="text"
                                placeholder="Short sleeve t-shirt"
                                value={form.name}
                                onChange={handleChange}
                            />
                        </div>

                        {/* DESCRIPTION */}
                        <div className="shopowner_field">
                            <label className="shopowner_label">Description</label>
                            <textarea
                                className="shopowner_textarea"
                                data-agent="shopowner-product-description-input"
                                name="description"
                                placeholder="Describe your product..."
                                value={form.description}
                                onChange={handleChange}
                            />
                        </div>

                        {/* IMAGE URL */}
                        <div className="shopowner_field">
                            <label className="shopowner_label">Image</label>
                            <input
                                className="shopowner_input"
                                data-agent="shopowner-product-image-input"
                                name="image"
                                type="text"
                                placeholder="/images/SneakerShopItems/akwaocha.png"
                                value={form.image}
                                onChange={handleChange}
                            />
                            <div className="shopowner_image_preview_wrapper">
                                {form.image.trim()
                                    ? <img
                                        src={`${form.image}`}
                                        alt="Product preview"
                                        className="shopowner_image_preview"
                                      />
                                    : <span className="shopowner_image_preview_empty">Image preview will appear here</span>
                                }
                            </div>
                        </div>

                        {/* PRICE */}
                        <div className="shopowner_field">
                            <label className="shopowner_label">Price</label>
                            <div className="shopowner_price_wrapper">
                                <span className="shopowner_price_symbol">₦</span>
                                <input
                                    className="shopowner_price_input"
                                    data-agent="shopowner-product-price-input"
                                    name="price"
                                    type="number"
                                    placeholder="0.00"
                                    value={form.price}
                                    onChange={handleChange}
                                />
                            </div>
                        </div>

                        {/* SUBMIT */}
                        <div className="shopowner_actions">
                            <button
                                className="shopowner_add_product_btn"
                                data-agent="shopowner-submit-product-button"
                                onClick={handleSubmit}
                            >
                                Add product
                            </button>
                        </div>

                    </div>
                    <AgentChat />
                </main>
            </div>
        </div>
    );
}