import "./chatbot.css"
import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import { useNavigate } from "react-router-dom"
import { createHistory, addMessageToHistory, fetchHistory, fetchHistoryById } from "../../services/HistoryService";



export default function ChatBot() {
        const [ isAuthenticated, setIsAuthenticated ] = useState(null);
        const [ loading, setLoading ] = useState(true);
        const [ histories, setHistories ] = useState(null);
        const [ currentHistory, setCurrentHistory ] = useState([]);
        const [ messages, setMessages ] = useState([]);
        const [ inputText, setInputText ] = useState("");
        const [ loadingAIResponse, setLoadingAIResponse ] = useState(false);

        const navigate = useNavigate();
        
        useEffect(() => {   
            Promise.all([
                createHistory().then((response) => {
                    if (response.status === 201) {
                        setCurrentHistory(response.data);
                        setIsAuthenticated(true);
                    } else {
                        setIsAuthenticated(false);
                    }
                }).catch(() => {
                    setIsAuthenticated(false);
                }),
                
                fetchHistory().then((response) => {
                    if (response.status === 200) {
                        setHistories(response.data);
                    }
                }).catch(() => {
                    setHistories([]);
                })
            ]).finally(() => {
                setLoading(false);
            });
        }, []);
    
        const handleSendMessage = () => {
            if (loadingAIResponse)
                return;
            if (inputText.trim()) {
                setMessages(prev => [...prev, { text: inputText, sender: "user" }]);
                setInputText("");
                setLoadingAIResponse(true);
                addMessageToHistory(currentHistory.id, inputText).then((response) => {
                    if (response.status === 200 && response.data?.messages) {
                        const formattedMessages = response.data.messages.map((msg) => ({
                            text: msg.content,
                            sender: msg.role === "assistant" ? "bot" : "user"
                        }));
                        setMessages(formattedMessages);
                    }
                }).catch((error) => {
                    console.error("Error sending message:", error);
                }).finally(() => {
                    setLoadingAIResponse(false);
                });
            }
        };

        const changeHistory = (history) => {
            setCurrentHistory(history);
            const currentMessages = fetchHistoryById(history.id).then((response) => {
                if (response.status === 200 && response.data?.messages) {
                    if (!Array.isArray(response.data.messages)) {
                        setMessages([]);
                        return;
                    }
                    if(response.data.messages.length === 0)
                    {
                        setMessages([]);
                        return;
                    }
                    setMessages(response.data.messages.map((msg) => ({
                        text: msg.content,
                        sender: msg.role === "assistant" ? "bot" : "user"
                    })));
                }
            }).catch((error) => {
                console.error("Error fetching history by ID:", error);
            });
        };

        const handleKeyPress = (e) => {
            if (e.key === "Enter") {
                handleSendMessage();
            }
        };

        if (loading) {
            return <div>Loading...</div>;
        }
        if (!isAuthenticated) {
            navigate("/login");
            return null;
        }

    return (
        <div className="chats-container">
            <section className="chats-list">
                <h3>Historiques</h3>
                {histories && histories.map((history) => (
                    <button key={history.id} className="chat-item" onClick={() => changeHistory(history)} disabled={currentHistory.id === history.id || loadingAIResponse}>
                        <span>{history.name}</span>
                    </button>
                ))}
            </section>
            <section className="chat">
                <div className="messages-container">
                    {messages.length > 0 ? messages.map((message, index) => (
                        <div key={index} className={`message ${message.sender}`}>
                            <ReactMarkdown>{message.text}</ReactMarkdown>
                        </div>
                )) : <div className="no-messages">Aucun message pour le moment. Commencez la conversation !</div>}
                </div>
                
                <div className="input-container">
                    <input
                        type="text"
                        className="prompt-input"
                        placeholder="Écrivez votre message..."
                        value={inputText}
                        onChange={(e) => setInputText(e.target.value)}
                        onKeyUp={handleKeyPress}
                    />
                    <button className="send-button" onClick={handleSendMessage} disabled={loadingAIResponse}>
                        Envoyer
                    </button>
                </div>
            </section>
        </div>
    )
}