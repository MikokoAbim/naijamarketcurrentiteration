import { useEffect, useState } from 'react';
import '../styles/pages/Home.css';
import { useParams, useNavigate } from 'react-router-dom';
import { getShopOwnerById } from '../api/shop_owner';

import '../styles/pages/Shop_Owner.css';
import AgentChat from '../components/AgentChat';

export default function ShopOwnerShopCreate(){
    const {shopOwnerId} = useParams();

    const[shop_owner, setShopOwner] = useState(null)
    const[shop_name, setShopName] = useState("")
    const [shop_image, setShopImage] = useState("")
    const[shop, setShop] = useState(null)
    const navigate = useNavigate();

    useEffect(() => {
        getShopOwnerById(shopOwnerId).then(data => {
            setShopOwner(data)
        });
    }, [shopOwnerId]);

    const handleCreateShop = async () => {
        if (!shop_name.trim() || !shop_image.trim()) return;

        const response = await fetch("http://127.0.0.1:8000/naija_market/shop_owner/create_shop", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                name: shop_name,
                image: shop_image,
                shop_owner_id: shopOwnerId,
            })
        });

        const data = await response.json();
        
        if(data){
            const updatedShopOwner = await getShopOwnerById(shopOwnerId);
            setShopOwner(updatedShopOwner);
        }
    };

    if (!shop_owner) return <div>Loading...</div>;


    return(
        <div className='page'>
            <aside className = "sidebar">
                <div className="sidebar-logo">Logo</div>
                <div className="sidebar-item active" data-agent="nav-home" onClick={() => navigate("/")}>Home</div>
                <div className="sidebar-item" data-agent="nav-cart">Cart</div>
                <div className="sidebar-bottom" data-agent="nav-signin">Sign in</div>
            </aside>

            <div className='shopowner_content'>
                <main className='shopowner_main'>
                    <div className='shopowner_greeting'>
                        Hello <span>{shop_owner.name}</span> — ready to set up your shop?
                    </div>

                    <div className='shopowner_card'>
                        <div className='shopowner_section_label'>
                            {shop_owner.shop ? shop_owner.shop.name: "Add store name"}
                            {!shop_owner.shop && <span className='shopowner_edit_icon'>✏️</span>}
                        </div>

                        {!shop_owner.shop && (
                            <div className='shopowner_name_row'>
                                <input
                                    className='shopowner_name_input'
                                    data-agent="shopowner-add-shop-name-input"
                                    type="text"
                                    placeholder="What is your shop name?"
                                    value={shop_name}
                                    onChange={e => setShopName(e.target.value)}
                                />
                                <input
                                    className='shopowner_name_input'
                                    data-agent="shopowner-add-shop-image-input"
                                    type="text"
                                    placeholder="/images/SneakerShopItems/akwaocha.png"
                                    value={shop_image}
                                    onChange={e => setShopImage(e.target.value)}
                                />

                                {/* PREVIEW — shows as soon as a url is typed */}
                                <div className='shopowner_image_preview_wrapper'>
                                    {shop_image.trim()
                                        ? <img
                                            src={`${shop_image}`}
                                            alt="Shop preview"
                                            className='shopowner_image_preview'
                                        />
                                        : <span className='shopowner_image_preview_empty'>Image preview will appear here</span>
                                    }
                                </div>

                                <button
                                    className='shopowner_name_btn'
                                    data-agent="shopowner-add-shop-name-button"
                                    onClick={handleCreateShop}
                                    disabled={!shop_name.trim() || !shop_image.trim()}
                                >
                                    Create shop
                                </button>
                            </div>
                        )}


                        <div className='shopowner_product_placeholder'>
                            <div className='shopowner_product_placeholder_icon'>🏷️</div>
                            <div className='shopowner_product_placeholder_text'>Add your first product</div>
                            <div className='shopowner_product_placeholder_sub'>
                                Create your shop first, then start adding products
                            </div>
                        </div>

                        <div className='shopowner_actions'>
                            <button
                                className='shopowner_add_product_btn'
                                data-agent = "shopowner-add-product-button"
                                disabled = {!shop_owner.shop?.name || !shop_owner.shop?.image}
                                onClick={() => navigate(`/shop-owner/${shopOwnerId}/add-product`)}
                            >
                                Add product to your shops
                            </button>
                        </div>    
                    </div>
                    <AgentChat />
                </main>
            </div>
        </div>
    )
}