import {useParams} from "react-router-dom"
import { useState, useEffect } from "react";
import { getShopById } from "../api/shop";
import { useNavigate } from "react-router-dom";
import AgentChat from '../components/AgentChat';

import '../styles/pages/Home.css';
import '../styles/pages/Shop.css';



export default function Shop(){
    const[shop, setShop] = useState(null);
    const {shopId} = useParams();
    const navigate = useNavigate();

    useEffect(() => {
        getShopById(shopId).then(data => {
            setShop(data)
        });
    }, [shopId]);

    if (!shop) {
        return <div>Loading...</div>;
    }

    return(
        <div className="page">
            <aside className = "sidebar">
                <div className="sidebar-logo">Logo</div>
                <div className="sidebar-item active" data-agent="nav-home" onClick={() => navigate("/")}>Home</div>
                <div className="sidebar-item" data-agent="nav-cart">Cart</div>
                <div className="sidebar-bottom" data-agent="nav-signin">Sign in</div>
            </aside>

            <div className="main_shop_content">
                <main className="main_shop">
                    <section className="main_shop_hero">
                        <div className="main_shop_hero_logo">{shop.name}</div>
                        <div className='main_shop_hero_search_wrapper'>
                                <input 
                                    className="main_shop_hero_search_box" 
                                    data-agent="shop-search-input"
                                    type = "text"
                                    placeholder='What are you looking for?'
                                />
                                <button 
                                    className = "main_shop_hero_search_btn" 
                                    data-agent="shop-search-button"
                                    onClick={() => {
                                        handleSearch();
                                    }}>
                                    ➜
                                </button>
                            </div>
                    </section>

                    <section className="main_shop_filters">
                        <div className="main_shop_chip" data-agent="chip-home">General filter</div>
                        <div className="main_shop_chip" data-agent="chip-women">Arrange by Price</div>
                        <div className="main_shop_chip" data-agent="chip-men">Arrange by Colour</div>
                        <div className="main_shop_chip" data-agent="chip-beauty">Arrange by Reviews</div>
                    </section>

                    <section className="main_shop_products">
                        <div className="main_shop_products_grid">
                            {shop.items.map((item) => (
                                <div
                                    className="main_shop_product_card"
                                    data-agent = {`item-${item.id}`}
                                    key = {item.id}
                                    onClick={() => navigate(`/item/${item.id}`)}
                                >
                                    <img src = {item.image} className="main_shop_product_image" />
                                    <div className="main_shop_product_info">
                                        <div className="main_shop_product_name">{item.name}</div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </section>
                    <AgentChat />
                </main>
            </div>
        </div>
    )
}