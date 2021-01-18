public static void Run(Stream myBlob, string name, string myInputBlob, out string myOutputBlob, ILogger log)
{
    log.LogInformation($"C# Blob trigger function Processed blob - Name: '{name}', Size: {myBlob.Length} Bytes");
    myOutputBlob = myInputBlob;
}