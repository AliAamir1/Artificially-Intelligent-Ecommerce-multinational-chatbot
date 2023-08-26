import React, { useState } from "react";
import axios from "axios";
import { Container, TextField, Button } from "@mui/material";

function Chatbot() {
  const [messages, setMessages] = useState([
    {
      text: "ROBO: My name is Robo. I will answer your queries.",
      sender: "bot",
    },
  ]);
  const [input, setInput] = useState("");

  const handleInput = async (e) => {
    e.preventDefault();

    const response = await axios.post("http://127.0.0.1:5000/chatbot", {
      user_response: input,
    });

    const botResponse = response.data.response;
    const newBotMessages = [
      ...messages,
      { text: input, sender: "user" },
      { text: botResponse, sender: "bot" },
    ];
    setMessages(newBotMessages);
    setInput("");
    e.target.value = "";
  };

  return (
    <Container
      maxWidth="sm"
      sx={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        mt: 10,
      }}
    >
      <h1>Chat Us</h1>
      <div
        style={{
          height: 400,
          width: "100%",
          border: "1px solid black",
          overflow: "scroll",
          marginBottom: "1rem",
          padding: "1rem",
        }}
      >
        {messages.map((message, index) => (
          <p
            key={index}
            style={{
              textAlign: message.sender === "bot" ? "left" : "right",
            }}
          >
            {message.sender === "bot" ? "" : ""}
            {message.text}
          </p>
        ))}
      </div>
      <form onSubmit={handleInput} style={{ width: "100%", display: "flex" }}>
        <TextField
          label="User Input"
          variant="outlined"
          fullWidth
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />

        <Button variant="contained" type="submit" sx={{ ml: 1 }}>
          Send
        </Button>
      </form>
    </Container>
  );
}

export default Chatbot;
