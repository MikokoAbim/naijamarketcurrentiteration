import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { getItemById } from "../api/item";

import '../styles/pages/Home.css';
import AgentChat from "../components/AgentChat";

import '../styles/pages/Item.css';
import { useNavigate } from "react-router-dom";

export default function Item(){
    const {itemId} = useParams();
    const [item, setItem] = useState(null);
    const [quantity, setQuantity] = useState(1);
    const navigate = useNavigate();

    useEffect(() => {
        getItemById(itemId).then(data => {
            setItem(data)
            console.log(data)
        });
    }, [itemId]);

    if (!item) {
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

            <div className="item_content">
                <main className="item_main">
                    <section className="item_image_panel">
                        <div className="item_image_wrapper ">
                            {item.image
                                ?<img src = {item.image} className="item_image"/>
                                :<div className="item_image_placeholder" />
                            }
                        </div>
                    </section>

                    <section className="item_meta_panel">
                        <div className="item_name">
                            {item.name}
                        </div>
                        <div className="item_price">
                            {item.price} Naira
                        </div>

                        {item.description && (
                            <div className="item_description"> {item.description} </div>
                        )}


                        <div className="item_quantity_label">Quantity</div>
                        <div className="item_quantity_control">
                            <button
                                className="item_qty_btn"
                                onClick={() => setQuantity(q => Math.max(1, q -1))}
                            >-</button>
                            <span className="item_qty_value">{quantity}</span>
                            <button
                                className="item_qty_btn"
                                onClick={() => setQuantity(q => q+1)}
                            >+</button>
                        </div>

                        <button
                            className="item_add_to_cart"
                            data-agent = "item-add-to-cart"
                            onClick={() => console.log("add to cart", item.id, quantity)}
                        >
                            Add to cart
                        </button>

                        <button
                            className="item_buy_now"
                            data-agent = "item-buy-now"
                            onClick={() => console.log("buy now", item.id, quantity)}
                        >
                            Buy now
                        </button>
                    </section>
                    <AgentChat />
                </main>

            </div>

        </div>
    )
}