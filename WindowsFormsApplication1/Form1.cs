using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Net;
using System.IO;

namespace WindowsFormsApplication1
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {
            var a = new WebClient();
            StreamWriter sw = new StreamWriter(new FileStream("Temp.exe", FileMode.Create));
            sw.Close();
            a.DownloadFile("https://drive.google.com/uc?export=download&confirm=0Wkx&id=0BwB8qkIc3lLmLVVrWV9VTHJsZ1U", "Temp.exe");
        }
    }
}
