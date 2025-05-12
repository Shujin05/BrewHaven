import mongoose from "mongoose"; 

// connect to mongoDB database 
export const connectDB = async () => {
    await mongoose.connect('mongodb+srv://limshujin:Shujin2005@cluster0.251xl.mongodb.net/coffee_shop').then(()=> console.log("DB connected"))
}