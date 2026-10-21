import '../styles/pages/Home.css';
import AgentChat from '../components/AgentChat';
import { useEffect, useState } from 'react';
import { getMarketplace, getShopByName } from '../api/market_place';

import {useNavigate} from "react-router-dom";

export default function Home(){
    const[allShops, setAllShops] = useState([]);
    const[shops, setShops] = useState([]);
    const[search, setSearch] = useState("");
    const naviagate = useNavigate();

    useEffect(() => {
        getMarketplace().then(data => {
            setAllShops(data.shops);
            setShops(data.shops);
        });
    }, []);

    const handleSearch = async () => {
        if (search.trim() === "") {
            setShops(allShops);
            return;
        }

        const result = await getShopByName(search);

        if(Array.isArray(result)){
            setShops(result);
        }else{
            setShops([]);
        }
    };

    useEffect(() => {
        if (search.trim() === "") {
            setShops(allShops);
        }
    }, [search, allShops]);

    return(
        <div className="page">
            <aside className = "sidebar">
                <div className="sidebar-logo">Logo</div>
                <div className="sidebar-item active" data-agent="nav-home" onClick={() => naviagate("/")}>Home</div>
                <div className="sidebar-item" data-agent="nav-cart">Cart</div>
                <div className="sidebar-bottom" data-agent="nav-signin">Sign in</div>
            </aside>

            <div className="content">
                <header className="topbar">Top bar</header>

                <main className="main">
                    <section className="hero">
                        <div className="floating-card card-1"></div>
                        <div className="floating-card card-2"></div>
                        <div className="hero-center">
                            <div className="hero-logo">Naija Market</div>
                            <div className='search-wrapper'>
                                <input 
                                    className="search-box" 
                                    data-agent="search-input"
                                    type = "text"
                                    placeholder='Search shops....'
                                    value={search}
                                    onChange={(e) => setSearch(e.target.value)}
                                    onKeyDown={(e) =>  {if(e.key === "Enter") handleSearch();}}
                                />
                                <button 
                                    className = "search-btn" 
                                    data-agent="search-button"
                                    onClick={() => {
                                        handleSearch();
                                    }}>
                                    ➜
                                </button>
                            </div>
                        </div>
                    </section>

                    <section className="chips">
                        <div className="chip" data-agent="chip-women">Women</div>
                        <div className="chip" data-agent="chip-men">Men</div>
                        <div className="chip" data-agent="chip-beauty">Beauty</div>
                        <div className="chip" data-agent="chip-home">Home</div>
                        <div className="chip" data-agent="chip-fitness">Fitness</div>
                    </section>

                    <section className="grid-section">
                        <div className="card-grid">
                            
                            {shops.map((shop) => (
                                <div 
                                    className='shop-grid' key = {shop.id} 
                                    data-agent={`shop-${shop.id}`} 
                                    onClick={() => naviagate(`/shop/${shop.id}`)}
                                >
                                    <div className="shop-name">{shop.name}</div>
                                    <img src={shop.image} />
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