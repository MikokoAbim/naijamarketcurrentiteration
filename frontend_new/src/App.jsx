import Home from "./pages/Home2";
import Shop from "./pages/Shop";
import Item from "./pages/Item";
import {BrowserRouter, Routes, Route} from "react-router-dom";
import ShopOwnerShopCreate from "./pages/Shop_Owner_Shop_Create";
import ShopOwnerProductAdd from "./pages/Shop_Owner_Product_Add";

export default function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element = {<Home />}/>
                <Route path="/shop/:shopId" element = {<Shop />}/>
                <Route path="/item/:itemId" element = {<Item />}/>
                <Route path="/shop-owner/:shopOwnerId/create" element = {<ShopOwnerShopCreate />}/>
                <Route path="/shop-owner/:shopOwnerId/add-product" element = {<ShopOwnerProductAdd />}/>
            </Routes>
        </BrowserRouter>
    );
}