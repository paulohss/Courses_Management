import { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import assistantIcon from '../images/assistant.png';
import userIcon from '../images/user.png';

export default function ChatBotSql({ isOpen, onClose }) {


    //  List of messages
    const [messages, setMessages] = useState([
        {
            content: "Hi, I'm your Courses Management Assistant. I can help you retrive information from the database.",
            role: "assistant"
        },
        {
            content: "How can I help you today?",
            role: "assistant"
        }
    ]);
    
    //  State to check if the assistant is typing
    const [isTyping, setIsTyping] = useState(false);

    // Reference to the last message
    const messagesEndRef = useRef(null);


    //--------------------------------------------------------------------------------
    // Function to handle Enter key press
    //--------------------------------------------------------------------------------
    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault(); // Prevent default behavior (newline)
            const form = e.target.form;
            if (form) {
                form.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
            }
        }
    };

    //--------------------------------------------------------------------------------
    // Function to scroll to the bottom of the chat
    //--------------------------------------------------------------------------------
    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }

    //--------------------------------------------------------------------------------
    // Scroll to the bottom of the chat when a new message is added
    //--------------------------------------------------------------------------------
    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    //--------------------------------------------------------------------------------
    //  Function to handle form submission:
    //--------------------------------------------------------------------------------    
    const handleSubmit = async (e) => {
        e.preventDefault();
        const newMessage = {
            content: e.target[0].value,
            role: "user"
        }
        const newMessages = [...messages, newMessage];
        setMessages(newMessages);
        setIsTyping(true);
        e.target.reset();

        try {
            const response = await axios.post('http://127.0.0.1:5000/api/sqlchatbot/ask', {
                message: newMessage.content
            });

            setMessages([...newMessages, {
                content: response.data.response,
                role: "assistant"
            }]);
        } catch (error) {
            console.error('Error:', error);
        }
        setIsTyping(false);
    }

    //--------------------------------------------------------------------------------
    // Render the component:
    //--------------------------------------------------------------------------------       
    return (
        <dialog id="chatbot_modal" className="modal bg-black/40" open={true}>
            <div className="modal-box w-11/12 max-w-5xl h-[80vh] flex flex-col">
                <button className="btn btn-sm btn-circle btn-ghost absolute right-2 top-2" onClick={onClose}>✕</button>
                <h3 className="font-bold text-lg py-4">Courses Management Assistant</h3>
                <div className="divider divider-secondary"></div>
                <div className='flex-grow overflow-auto p-4'>
                    {messages.map((msg, i) => (
                        <div className={`chat ${msg.role === 'assistant' ? 'chat-start' : 'chat-end'}`} key={'chatKey' + i}>
                            <div className="chat-image avatar">
                                <div className="w-10 rounded-full">
                                    <img
                                        src={msg.role === 'assistant' ? assistantIcon : userIcon}
                                        alt={msg.role}
                                    />
                                </div>
                            </div>
                            <div className="chat-bubble">{msg.content}</div>
                        </div>
                    ))}
                    <div ref={messagesEndRef} />
                </div>

                <form className="form-control mt-4" onSubmit={handleSubmit}>
                    <div className="input-group relative">
                        {isTyping && <small className='absolute -top-8 left-0.5 animate-pulse text-green-400 text-lg'>Assistant is typing...</small>}
                        <textarea
                            placeholder="Type your question..."
                            className="textarea textarea-bordered textarea-lg w-[calc(100%-4rem)]"
                            onKeyDown={handleKeyDown}
                        ></textarea>
                        <button className="btn btn-square w-16" type="submit">
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="currentColor" viewBox="0 0 16 16">
                                <path d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11ZM6.636 10.07l2.761 4.338L14.13 2.576 6.636 10.07Zm6.787-8.201L1.591 6.602l4.339 2.76 7.494-7.493Z" />
                            </svg>
                        </button>
                    </div>
                </form>
            </div>
        </dialog>
    );
}