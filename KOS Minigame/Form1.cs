﻿using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace WindowsFormsApplication2
{
    public partial class Form1 : Form
    {
        public static long point = 0;
        public int clickPerPoint = 1;
        public int secondPerPoint = 0;

        public Form1()
        {
            InitializeComponent();
            label2.Text = point.ToString();
            label4.Text = clickPerPoint.ToString();
            label6.Text = secondPerPoint.ToString();
        }

        private void timer1_Tick(object sender, EventArgs e)
        {
            point += secondPerPoint;
            label2.Text = point.ToString();
        }

        private void button3_Click(object sender, EventArgs e)
        {
            point += clickPerPoint;
        }

        private void button1_Click(object sender, EventArgs e)
        {
            clickPerPoint++;
            point -= clickPerPoint *= 2;
        }

        private void button2_Click(object sender, EventArgs e)
        {
            secondPerPoint++;
            point -= secondPerPoint *= 3;
        }
    }
}
