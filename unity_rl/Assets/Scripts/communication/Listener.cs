using System;
using NetMQ;
using NetMQ.Sockets;



namespace ReqRep
{
    public class Listener
    {
        private readonly string _host;
        private readonly string _port;
        private readonly Action<string> _messageCallback;

        public Listener(string host, string port, Action<string> messageCallback)
        {
            _host = host;
            _port = port;
            _messageCallback = messageCallback;
        }
        
        public void RequestMessage()
        {
            while(true)
            {
                Random r = new Random();
               
                var messageReceived = false;
                var message = "";
                AsyncIO.ForceDotNet.Force();

                using (var socket = new RequestSocket())
                {
                    socket.Connect($"tcp://{_host}:{_port}");
                    if (socket.TrySendFrame("testing" + r.Next(100)))
                    {
                        messageReceived = socket.TryReceiveFrameString(TimeSpan.FromSeconds(120),out message);
                    }
                    else
                    {
                        message = "cant send message ";
                    }
                }

                NetMQConfig.Cleanup();
                if (!messageReceived)
                    message = "Could not receive message from server!";
                _messageCallback(message);
            }
        }

           
    }
}