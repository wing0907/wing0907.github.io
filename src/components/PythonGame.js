import React, { useEffect, useState } from 'react';
import io from 'socket.io-client';

const socket = io('http://localhost:5000'); // Adjust if hosted remotely

function PythonGame() {
    const [image, setImage] = useState('');

    useEffect(() => {
        socket.on('connect', () => {
            console.log('Connected to Flask server');
            socket.emit('start_game'); // Start the game when connected
        });

        socket.on('game_frame', (data) => {
            setImage(`data:image/png;base64,${data.image}`);
        });

        return () => {
            socket.disconnect();
        };
    }, []);

    return (
        <div>
            <h1>Python Game in React</h1>
            {image ? <img src={image} alt="Game frame" /> : <p>Loading...</p>}
        </div>
    );
}

export default PythonGame;
