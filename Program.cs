using System;
using System.Net;
using System.Text;

class Program
{
    static void Main()
    {
        HttpListener listener = new HttpListener();
        listener.Prefixes.Add("http://localhost:3000/");
        listener.Start();
        Console.WriteLine("Listening on port 3000...");

        while (true)
        {
            HttpListenerContext context = listener.GetContext();
            HttpListenerRequest request = context.Request;
            HttpListenerResponse response = context.Response;
            string responseString = "Hello World";

            if (request.HttpMethod == "POST")
            {
                using (var reader = new System.IO.StreamReader(request.InputStream, request.ContentEncoding))
                {
                    string postData = reader.ReadToEnd();
                    Console.WriteLine("Received POST data: " + postData);
                }
            }

            byte[] buffer = Encoding.UTF8.GetBytes(responseString);
            response.ContentLength64 = buffer.Length;
            System.IO.Stream output = response.OutputStream;
            output.Write(buffer, 0, buffer.Length);
            output.Close();
        }
    }
}
