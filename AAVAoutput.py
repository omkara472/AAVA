using System;

namespace SampleDotNetApp
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Hello, this is a sample .NET application!");
            Console.WriteLine("Current Date and Time: " + DateTime.Now);

            int a = 10;
            int b = 20;
            int sum = a + b;

            Console.WriteLine($"Sum of {a} and {b} is {sum}");
            Console.WriteLine("Press any key to exit...");
            Console.ReadKey();
        }
    }
}
