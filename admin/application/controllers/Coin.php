<?php if(!defined('BASEPATH')) exit('No direct script access allowed');

require APPPATH . '/libraries/BaseController.php';

/**
 * Class : User (UserController)
 * User Class to control all user related operations.
 * @author : Kishor Mali
 * @version : 1.1
 * @since : 15 November 2016
 */
class Coin extends BaseController
{
    /**
     * This is default constructor of the class
     */
    public function __construct()
    {
        parent::__construct();
        $this->load->model('model_coin_info');
        $this->isLoggedIn();   
    }
    /**
     * This function is used to show users profile
     */
    function coin_info($active = "BTC")
    {
        $data["active"] = $active;
        $coinInfos = $this->model_coin_info->get_coin_info();
        $newArray = array();
        foreach($coinInfos as $coinInfo)
        {
            if(!isset($newArray[$coinInfo->quoteAsset]))
            {
                 $newArray[$coinInfo->quoteAsset] = array();
            }
        
            $newArray[$coinInfo->quoteAsset][] = $coinInfo;
        }
        $data['coinInfo'] = $newArray;
        $this->global['pageTitle'] = "Coin Info";
        $this->loadViews("coinInfo", $this->global, $data, NULL);
    }
    /**
     * This function is used to update the user details
     * @param text $active : This is flag to set the active tab
     */
    function changeCoinPredict($active = "BTC")
    {
        $input_data = $this->input->post(); // == 'on' ? 1 : 0;
        $data = array();
        foreach ($input_data as $key => $value){
            $coinInfo = array(
                'id' => $key ,
                'isPrediction' => $value == 'on' ? 1 : 0
            );
            $data[] = $coinInfo;
        }
        $result = $this->model_coin_info->update_coin_info($data);
        if($result == true)
        {
            $this->session->set_flashdata('success', 'Coin info prediction update success and retrain after 5 minutes');
        }

        redirect('coin_info/'.$active);
    }

    function configTable()
    {
        $table = $this->model_coin_info->get_columns();
        $data['table'] = $table;
        $this->global['pageTitle'] = "Config table";
        $this->loadViews("configTable", $this->global, $data, NULL);
    }

    function changeTable()
    {
        $input_data = $this->input->post(); // == 'on' ? 1 : 0;
        $data = array();
        foreach ($input_data as $key => $value){
            $coinInfo = array(
                'id' => $key ,
                'hide' => $value == 'on' ? 1 : 0
            );
            $data[] = $coinInfo;
        }
        $result = $this->model_coin_info->update_columns_show($data);
        $this->changeFileJson();
        if($result == true)
        {
            $this->session->set_flashdata('success', 'Change show/hide columns update success and retrain after 5 minutes');
        }

        redirect('configTable');
    }

    function configHomeListing()
    {
        if($this->isAdmin() == TRUE) {
            $this->loadThis();
        }
        else {        
            $data['configIndex'] = $this->model_coin_info->get_config_index();
            $this->global['pageTitle'] = 'CPPTS : Config Home page';            
            $this->loadViews("homePage", $this->global, $data, NULL);
        }
    }

    function editTitleOld($userId = NULL)
    {        
        $data['data'] = $this->model_coin_info->get_config_index_only();        
        $this->global['pageTitle'] = 'CPPTS : Edit Title, Email';        
        $this->loadViews("configHome", $this->global, $data, NULL);
    }

    function editTitle()
    {
        $data = $this->model_coin_info->get_config_index_only();
        $input_data = $this->input->post();
        $data_update = array($input_data);
        if (isset($data_update[0]['title']) && $data->title != $data_update[0]['title']){
            $this->changeFileHtml($data->title, $data_update[0]['title']);
            $this->model_coin_info->resetTrain();
        }
        $this->model_coin_info->update_config_index($data_update);
        $this->changeFileJson();
        $this->global['pageTitle'] = 'CPPTS : Config Home page';       
        redirect('configHome');
    }

    function addWallet()
    {
        if($this->isAdmin() == TRUE) {
            $this->loadThis();
        }
        else {        
            $this->global['pageTitle'] = 'CPPTS : Add Wallet'; 
            $this->loadViews("addWallet", $this->global, NULL, NULL);
        }
    }

    function changeFileJson(){        
        $path_json = $_SERVER['DOCUMENT_ROOT'] . "/bootstrap/footer.json";
        $data = $this->model_coin_info->get_config_index();
        $columns = $this->model_coin_info->get_columns();
        $donate = array();
        foreach ($data as $item){
            $donate[] = array(
                'name'=> $item->name,
                'wallet'=> $item->wallet
            );
        }
        $show_columns = array();
        foreach($columns as $column){
            $show_columns[] = $column->hide;
        }
        $response = array(
            'email' => $data[0]->email,
            'donate' => $donate,
            'hide_columns' => $show_columns
        );
        $fp = fopen($path_json, 'w');
        fwrite($fp, json_encode($response));
        fclose($fp);
    }

    function changeFileHtml($titleOld = '', $titleNew = ''){
        $path_json = $_SERVER['DOCUMENT_ROOT'] . "/index.html";
        $data = file_get_contents($path_json);
        $data = str_replace($titleOld, $titleNew, $data);
        file_put_contents($path_json, $data);

        $path_json = $_SERVER['DOCUMENT_ROOT'] . "/chart/chart.html";
        $data = file_get_contents($path_json);
        $data = str_replace($titleOld, $titleNew, $data);
        file_put_contents($path_json, $data);
    }
    function addNewWallet()
    {
        $input_data = $this->input->post();
        $data['configIndex'] = $this->model_coin_info->insert_donate($input_data);
        $this->changeFileJson();
        $this->global['pageTitle'] = 'CPPTS : Config Home page';        
        redirect('configHome');
    }


    function editWallet($name = 'BTC')
    {
        if($this->isAdmin() == TRUE) {
            $this->loadThis();
        }
        else {                
            $data['data'] = $this->model_coin_info->get_donate($name);            
            $this->global['pageTitle'] = 'CPPTS : Edit Wallet';            
            $this->loadViews("editWallet", $this->global, $data, NULL);
        }
    }

    function editWalletDB()
    {
        $input_data = $this->input->post();
        $data_update = array($input_data);
        $data['configIndex'] = $this->model_coin_info->update_donate($data_update);
        $this->changeFileJson();        
        redirect('configHome');
    }

    function deleteWallet() 
    {
        $name = $this->input->post('wallet');        
        $result = $this->model_coin_info->deleteWallet($name);            
        if ($result > 0) {
            $this->changeFileJson();
            echo(json_encode(array('status'=>TRUE))); 
        }
        else { 
            echo(json_encode(array('status'=>FALSE))); 
        }
    }
}

?>