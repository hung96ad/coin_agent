
<?php
header("Access-Control-Allow-Origin: *");
require APPPATH . '/libraries/REST_Controller.php';
use Restserver\Libraries\REST_Controller;

defined('BASEPATH') OR exit('No direct script access allowed');
/**
 * Created by PhpStorm.
 * User=> hungnt
 * Date=> 24/11/2018
 * Time=> 21:00
 */

class Coin_info extends REST_Controller
{

    public function index_get()
    {
        $this->load->model('model_coin_info');
        $reuslt = $this->model_coin_info->get_data();
        // $columes = $this->model_coin_info->get_columns();

        $re = array(
            // "columns" => $columes,
            "data" => $reuslt
        );

        $this->response($re
        , REST_Controller::HTTP_OK);
    }

    public function chart_get($symbol = 'BTCUSDT')
    {
        $this->load->model('model_coin_info');
        $reuslt = $this->model_coin_info->get_data();

        $re = array($reuslt);

        $this->response($re
        , REST_Controller::HTTP_OK);
    }
}