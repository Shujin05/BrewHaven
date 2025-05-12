import mongoose from "mongoose"; 

// create schema 
const orderSchema = new mongoose.Schema({
    userId: {type:String, required:true}, 
    items: {type:Array, required:true}, 
    amount: {type:Number, required: true}, 
    address:{type:Object, required:true}, 
    status:{type:String, default:"Preparing your order..."}, 
    date:{type:Date, default:Date.now()}, 
    payment:{type:Boolean, default:false}, 
})

// if orderModel is not in database, a new database is formed
const orderModel = mongoose.models.order || mongoose.model("order", orderSchema); 

export default orderModel; 