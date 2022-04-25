
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

class Chart extends REST_Controller
{
    public function index_get()
    {
        $symbol = $this->input->get('symbol', TRUE);
        if ($symbol)
        {
            $this->load->model('model_coin_info');
            $this->response($this->model_coin_info->get_chart($symbol), REST_Controller::HTTP_OK);
        }
    }
}