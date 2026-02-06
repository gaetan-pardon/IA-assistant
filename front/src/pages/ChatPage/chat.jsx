import "./chat.css";
import ChatBot from "../../components/chatbot/chatbot"; 

export default function ChatPage() {
    return (
        <div className="chat-component">
            <h1 className="chat-title">Chat 2GP</h1>
            <ChatBot />
        </div>
    )
}