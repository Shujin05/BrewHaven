import React, { useContext, useEffect, useState } from 'react'
import './PlaceOrder.css'
import { StoreContext } from '../../Context/StoreContext'
import { assets } from '../../assets/assets';
import { useNavigate } from 'react-router-dom';
import axios from "axios"

const PlaceOrder = () => {

    const { getTotalCartAmount, token, food_list, cartItems, url} = useContext(StoreContext);
    
    const [data, setData] = useState({
        firstName:"", 
        lastName:"", 
        email:"",
        street:"",
        city:"",
        state:"", 
        zipcode:"",
        country:"", 
        phone:"", 
    })

    const navigate = useNavigate();

    const onChangeHandler = (event) => {
        const name = event.target.name
        const value = event.target.value
        setData(data => ({ ...data, [name]: value }))
    }

    const placeOrder = async (event) => {
        event.preventDefault();
        let orderItems = [];
        food_list.map((item)=> {
            if (cartItems[item._id]>0) {
                let itemInfo = item; 
                itemInfo["quantity"] = cartItems[item._id]
                orderItems.push(itemInfo)
            }
        })
        let orderData = {
            address: data, 
            items: orderItems,
            amount: getTotalCartAmount() + 5,
        }
        let response = await axios.post(url+"/api/order/place", orderData, {headers:{token}})
        if (response.data.success) {
            const {session_url} = response.data; 
            window.location.replace(session_url)
        }
        else{
            alert("Error"); 
        }
    }
    useEffect(()=>{
        if (!token) {
            navigate('/cart')
        }
        else if (getTotalCartAmount === 0) {
            navigate('/cart')
        }
    }, [token])

    return (
        <form onSubmit={placeOrder} className='place-order'>
            <div className="place-order-left">
                <p className='title'>Delivery Information</p>
                <div className="multi-field">
                    <input required type="text" name='firstName' onChange={onChangeHandler} value={data.firstName} placeholder='First name' />
                    <input required type="text" name='lastName' onChange={onChangeHandler} value={data.lastName} placeholder='Last name' />
                </div>
                <input required type="email" name='email' onChange={onChangeHandler} value={data.email} placeholder='Email address' />
                <input required type="text" name='street' onChange={onChangeHandler} value={data.street} placeholder='Street' />
                <div className="multi-field">
                    <input type="text" name='city' onChange={onChangeHandler} value={data.city} placeholder='City' />
                    <input type="text" name='state' onChange={onChangeHandler} value={data.state} placeholder='State' />
                </div>
                <div className="multi-field">
                    <input required type="text" name='zipcode' onChange={onChangeHandler} value={data.zipcode} placeholder='Zip code' />
                    <input required type="text" name='country' onChange={onChangeHandler} value={data.country} placeholder='Country' />
                </div>
                <input type="text" name='phone' onChange={onChangeHandler} value={data.phone} placeholder='Phone' />
            </div>
            <div className="place-order-right">
                <div className="cart-total">
                    <h2>Cart Totals</h2>
                    <div>
                        <div className="cart-total-details"><p>Subtotal</p><p>${getTotalCartAmount()}</p></div>
                        <hr />
                        <div className="cart-total-details"><p>Delivery Fee</p><p>${getTotalCartAmount() === 0 ? 0 : 5}</p></div>
                        <hr />
                        <div className="cart-total-details"><b>Total</b><b>${getTotalCartAmount() === 0 ? 0 : getTotalCartAmount() + 5}</b></div>
                    </div>
                </div>
                <div className="payment-options">
                    <h2>Select Payment Method</h2>
                    <div className="payment-option">
                        <img src={assets.selector_icon} alt="" />
                        <p>COD ( Cash On Delivery )</p>
                    </div>
                    <button type="submit">PLACE ORDER</button>
                </div>

            </div>
        </form>
    )
}

export default PlaceOrder
