using System;
using System.Collections.Generic;
using System.Collections;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using CookComputing.XmlRpc;
using Microsoft.VisualBasic;

namespace Prueba_Webservice_Odoo
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        [XmlRpcUrl("")]
        public interface IOpenErpLogin : IXmlRpcProxy
        {
            [XmlRpcMethod("login")]
            int login(string dbName, string dbUser, string dbPwd);
            [XmlRpcMethod("logout")]
            int logout(string dbName, string dbUser, string dbPwd);
        }

        [XmlRpcUrl("")]
        public interface IOpenErp : IXmlRpcProxy
        {
            [XmlRpcMethod("execute")]
            int create(string dbName, int idUser, string dbPwd,string model, string method,XmlRpcStruct fieldValues);
            
            [XmlRpcMethod("execute")]
            int create(string dbName, int idUser, string dbPwd, string model, string method, XmlRpcStruct fieldValues, XmlRpcStruct otherFieldValues);
            
            [XmlRpcMethod("execute")]
            Object[] search(string dbName, int idUser, string dbPwd, string model, string method, Object[] filters);
            
            [XmlRpcMethod("execute")]
            bool write(string dbName, int idUser, string dbPwd, string model, string method, int[] ids, XmlRpcStruct fieldValues);
            
            [XmlRpcMethod("execute")]
            bool unlink(string dbName, int idUser, string dbPwd, string model, string method, object[] ids);
            
            [XmlRpcMethod("execute")]
            Object[] read(string dbName, int idUser, string dbPwd, string model, string method, object[] ids, object[] fields);

            [XmlRpcMethod("execute")]
            Object[] run_method(string dbName, int idUser, string dbPwd, string model, string method, object[] ids);

            [XmlRpcMethod("execute")]
            bool run_method2(string dbName, int idUser, string dbPwd, string model, string method, object[] ids);

        }

        int UserId;

        //Login
        private void button1_Click(object sender, EventArgs e)
        {
            //Login to openerp
            string usr = textBox2.Text.ToString();
            string pass = textBox3.Text.ToString();
            string db = textBox4.Text.ToString();

            IOpenErpLogin rpcClientLogin = XmlRpcProxyGen.Create<IOpenErpLogin>(); //add  XmlRpcProxyGen.CS File from src folder if required,
            rpcClientLogin.Url = "http://" + textBox1.Text.ToString() + ":8069/xmlrpc/common";
            UserId  = rpcClientLogin.login(db, usr, pass);
            richTextBox1.AppendText("Logueado como usuario con id: " + UserId.ToString() + " \r\n");

            

        }

        //Filtrar y leer
        private void button2_Click(object sender, EventArgs e)
        {

            IOpenErp rpcClient;
            string usr = textBox2.Text.ToString();
            string pass = textBox3.Text.ToString();
            string db = textBox4.Text.ToString();

            string model = textBox8.Text;

            rpcClient = XmlRpcProxyGen.Create<IOpenErp>();
            //Cambia la url a object para acceder a objetos
            rpcClient.Url = "http://" + textBox1.Text.ToString() + ":8069/xmlrpc/object";

            //Hacemos el metodo search con una lista de filtros vacia, nos devuelve todos los ids de res.partner
            ArrayList filter = new ArrayList();

            if (textBox5.Text != "" || textBox6.Text != "" || textBox7.Text != "")
            {
                ArrayList buscar = new ArrayList();

                buscar.Add(textBox5.Text);
                buscar.Add(textBox6.Text);
                buscar.Add(textBox7.Text);
                
                //filter es una tupla(array de arrays)
                filter.Add(buscar.ToArray());
            }
            var vids = rpcClient.search(db, UserId, pass, model, "search", filter.ToArray());

            ArrayList ids = new ArrayList();
            foreach (var id in vids)
                ids.Add((int)id);

            //ahora hacemos una lectura de campos con esos ids
            ArrayList campos = new ArrayList();
            campos.Add("name");
            campos.Add("is_company");

            var fields = rpcClient.read(db, UserId, pass, model, "read", ids.ToArray(), campos.ToArray());

            foreach (var field in fields)
                richTextBox1.AppendText("Id: " + ((XmlRpcStruct)field)["id"] + " -- Nombre: " + ((XmlRpcStruct)field)["name"] + " -- Es compañia: " + ((XmlRpcStruct)field)["is_company"] + " \r\n");


        }

        //Escribir
        private void button3_Click(object sender, EventArgs e)
        {
            IOpenErp rpcClient;
            string pass = textBox3.Text.ToString();
            string db = textBox4.Text.ToString();
            string model = textBox8.Text;

            rpcClient = XmlRpcProxyGen.Create<IOpenErp>();
            //Cambia la url a object para acceder a objetos
            rpcClient.Url = "http://" + textBox1.Text.ToString() + ":8069/xmlrpc/object";

            //Creamos un array de enteros para pasarle los ids
            int[] ides = new int[1];
            //Le asignamos el id del campo que queremos escribir
            ides[0] = (Convert.ToInt32(textBox9.Text));
            
            //Creamos el xmlstruct para pasar los campos y su valor
            XmlRpcStruct campos = new XmlRpcStruct();
            //Añadimos el nombre del campo y el nuevo valor que deseamos
            campos.Add(textBox10.Text,textBox11.Text );

            bool result = rpcClient.write(db, UserId, pass, model, "write", ides.ToArray(), campos);

            richTextBox1.AppendText("Respuesta write: " + result + " \r\n");

        }

        //Crear
        private void button4_Click(object sender, EventArgs e)
        {
            IOpenErp rpcClient;
            string pass = textBox3.Text.ToString();
            string db = textBox4.Text.ToString();
            string model = textBox8.Text;

            rpcClient = XmlRpcProxyGen.Create<IOpenErp>();
            //Cambia la url a object para acceder a objetos
            rpcClient.Url = "http://" + textBox1.Text.ToString() + ":8069/xmlrpc/object";

            //Creamos el xmlstruct para pasar los campos y su valor
            XmlRpcStruct campos = new XmlRpcStruct();
            //Añadimos el nombre de los campos y su valor
            campos.Add("name", textBox12.Text);
            campos.Add("is_company", "True");

            int result = rpcClient.create (db, UserId, pass, model, "create", campos);

            richTextBox1.AppendText("Id registro creado: " + result + " \r\n");
        }

        //Eliminar
        private void button5_Click(object sender, EventArgs e)
        {
            IOpenErp rpcClient;
            string pass = textBox3.Text.ToString();
            string db = textBox4.Text.ToString();
            string model = textBox8.Text;

            rpcClient = XmlRpcProxyGen.Create<IOpenErp>();
            //Cambia la url a object para acceder a objetos
            rpcClient.Url = "http://" + textBox1.Text.ToString() + ":8069/xmlrpc/object";

            ArrayList ids = new ArrayList();
            ids.Add(Convert.ToInt32(textBox13.Text));

            bool result = rpcClient.unlink (db, UserId, pass, model, "unlink", ids.ToArray ());

            richTextBox1.AppendText("Registro eliminado: " + result + " \r\n");
        }

        //Rellenar combos con ids de producto, y almacen
        private void button6_Click(object sender, EventArgs e)
        {
            IOpenErp rpcClient;
            string usr = textBox2.Text.ToString();
            string pass = textBox3.Text.ToString();
            string db = textBox4.Text.ToString();

            string model = textBox8.Text;

            rpcClient = XmlRpcProxyGen.Create<IOpenErp>();
            //Cambia la url a object para acceder a objetos
            rpcClient.Url = "http://" + textBox1.Text.ToString() + ":8069/xmlrpc/object";

            comboBox1.Items.Clear();
            comboBox2.Items.Clear();
            comboBox3.Items.Clear();

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
///// LLENADO DE COMBO 1
            //Buscamos los productos que son type = product(almacenables)
            ArrayList filter = new ArrayList();

                ArrayList buscar = new ArrayList();

                buscar.Add("type");
                buscar.Add("=");
                buscar.Add("product");
                
                //filter es una tupla(array de arrays)
                filter.Add(buscar.ToArray());

            var vids = rpcClient.search(db, UserId, pass, "product.product", "search", filter.ToArray());

            ArrayList ids = new ArrayList();
            foreach (var id in vids)
                ids.Add((int)id);

            //ahora hacemos una lectura de campos con esos ids
            ArrayList campos = new ArrayList();
            campos.Add("name");

            var fields = rpcClient.read(db, UserId, pass, "product.product", "read", ids.ToArray(), campos.ToArray());

            foreach (var field in fields)
                comboBox1.Items.Add(((XmlRpcStruct)field)["id"] + "- " + ((XmlRpcStruct)field)["name"]);

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
///// LLENADO DE COMBO 2 y 3
            //Ahora leemos los almacenes en stock.location

            ArrayList filter1 = new ArrayList();

            var vids1 = rpcClient.search(db, UserId, pass, "stock.location", "search", filter1.ToArray());

            ArrayList ids1 = new ArrayList();
            foreach (var id in vids1)
                ids1.Add((int)id);

            //ahora hacemos una lectura de campos con esos ids
            ArrayList campos1 = new ArrayList();
            campos1.Add("name");

            var fields1 = rpcClient.read(db, UserId, pass, "stock.location", "read", ids1.ToArray(), campos1.ToArray());

            foreach (var field in fields1)
                comboBox2.Items.Add(((XmlRpcStruct)field)["id"] + "- " + ((XmlRpcStruct)field)["name"]);
            
            foreach (var field in fields1)
                comboBox3.Items.Add(((XmlRpcStruct)field)["id"] + "- " + ((XmlRpcStruct)field)["name"]);
        }




        /// Funcion de boton de crear movimiento de almacen

        private void button7_Click(object sender, EventArgs e)
        {
            IOpenErp rpcClient;
            string pass = textBox3.Text.ToString();
            string db = textBox4.Text.ToString();
            string model = textBox8.Text;

            rpcClient = XmlRpcProxyGen.Create<IOpenErp>();
            //Cambia la url a object para acceder a objetos
            rpcClient.Url = "http://" + textBox1.Text.ToString() + ":8069/xmlrpc/object";

            //Creamos el xmlstruct para pasar los campos y su valor
            XmlRpcStruct campos = new XmlRpcStruct();
            //Añadimos el nombre de los campos y su valor (almenos los required son necesarios)




            string idCombo1 = comboBox1.Text.ToString().Substring(0, Strings.InStr(comboBox1.Text.ToString(), "-")-1);
            string idCombo2 = comboBox2.Text.ToString().Substring(0,Strings.InStr(comboBox2.Text.ToString(), "-")-1);
            //int idCombo2 = String.Compare(comboBox2.Text.ToString(),"-");
            string idCombo3 = comboBox3.Text.ToString().Substring(0, Strings.InStr(comboBox3.Text.ToString(), "-")-1);

            campos.Add("product_id", Convert.ToInt32(idCombo1 ));
            campos.Add("location_id", Convert.ToInt32(idCombo2));
            campos.Add("location_dest_id", Convert.ToInt32(idCombo3));
            campos.Add("name", textBox14.Text );
            campos.Add("product_uom_qty",Convert.ToDouble( textBox15.Text));
            campos.Add("invoice_state", "none");
            campos.Add("date_expected", "21/02/2015 01:29:23");
            //No son necesarios
            //campos.Add("date", "21/02/2015 01:29:23");
            //campos.Add("state", "draft");
            //campos.Add("priority", "1");
            //campos.Add("scrapped", false);
            //campos.Add("procure_method", "make_to_stock");
            //campos.Add("propagate", true);
            //campos.Add("partially_available", false);
            campos.Add("product_uom", 1);


            int result = rpcClient.create(db, UserId, pass, "stock.move", "create", campos);

            richTextBox1.AppendText("Movimiento de almacen creado: " + result + " \r\n");
        }



        private void button8_Click(object sender, EventArgs e)
        {
            IOpenErp rpcClient;
            string pass = textBox3.Text.ToString();
            string db = textBox4.Text.ToString();
            string model = textBox8.Text;

            rpcClient = XmlRpcProxyGen.Create<IOpenErp>();
            //Cambia la url a object para acceder a objetos
            rpcClient.Url = "http://" + textBox1.Text.ToString() + ":8069/xmlrpc/object";


            ArrayList ids = new ArrayList();
            ids.Add(Convert.ToInt32(textBox16.Text));
            
            //Esto de cancelar funciona
            //bool result = rpcClient.unlink(db, UserId, pass, "stock.move", "action_cancel", ids.ToArray());
            var result = rpcClient.run_method (db, UserId, pass, "stock.move", "action_confirm", ids.ToArray());
            
            //int result = rpcClient.create(db, UserId, pass, "stock.move", "action_done", campos);

            richTextBox1.AppendText("Movimiento de almacen confirmado: " + result[0] + " \r\n");
        }



        private void button9_Click(object sender, EventArgs e)
        {
            IOpenErp rpcClient;
            string pass = textBox3.Text.ToString();
            string db = textBox4.Text.ToString();
            string model = textBox8.Text;

            rpcClient = XmlRpcProxyGen.Create<IOpenErp>();
            //Cambia la url a object para acceder a objetos
            rpcClient.Url = "http://" + textBox1.Text.ToString() + ":8069/xmlrpc/object";


            ArrayList ids = new ArrayList();
            ids.Add(Convert.ToInt32(textBox16.Text));

            //Esto de cancelar funciona
            //bool result = rpcClient.unlink(db, UserId, pass, "stock.move", "action_cancel", ids.ToArray());
            bool result = rpcClient.run_method2(db, UserId, pass, "stock.move", "action_done", ids.ToArray());

            //int result = rpcClient.create(db, UserId, pass, "stock.move", "action_done", campos);

            richTextBox1.AppendText("Movimiento de almacen finalizado: " + result + " \r\n");
        }

    }
}
