<?php 
// var_dump($coinInfo);die;
?>
<div class="content-wrapper">
    <!-- Content Header (Page header) -->
    <section class="content-header">
        <h1>
            <i class="fa fa-user-circle"></i> Coin Info
            <small>View or modify information</small>
        </h1>
    </section>

    <section class="content">

        <div class="row">

            <div class="col-md-12">
                <div class="nav-tabs-custom">
                    <ul class="nav nav-tabs">
                    <?php foreach($coinInfo as $key => $value) { ?>
                        <li class="<?= ($active == $key)? "active" : "" ?>">
                            <a href="#<?php echo $key; ?>" data-toggle="tab"><?php echo $key; ?></a>
                        </li>
                    <?php }?>
                    </ul>
                    <div class="tab-content">
                    <?php foreach($coinInfo as $key => $coin) { ?>
                        <div class="<?= ($active == $key)? "active" : "" ?> tab-pane" id="<?php echo $key; ?>">
                            <form action="<?php echo base_url() . 'changeCoinPredict/' . $key;?>" method="post" role="form">
                                <div class="box-body">
                                    <?php foreach ($coin as $value) {?>
                                        <div class="col-md-3">
                                            <div class="checkbox">
                                                <label>
                                                <input type="hidden" name="<?php echo $value->id; ?>" value="0" />
                                                    <input type="checkbox" id='<?php echo $value->id; ?>' name='<?php echo $value->id; ?>' <?php echo $value->isPrediction == 1 ? "checked" : ""; ?> > <?php echo $value->symbol; ?>
                                                </label>
                                            </div>
                                        </div>
                                    <?php }?>
                                </div><!-- /.box-body -->
                                <div class="box-footer">
                                    <input type="submit" class="btn btn-primary" value="Submit" />
                                    <input type="reset" class="btn btn-default" value="Reset" />
                                </div>
                            </form>
                        </div>
                                    <?php } ?>
                    </div>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-md-12">
                <?php
                $this->load->helper('form');
                $error = $this->session->flashdata('error');
                if($error)
                {
                    ?>
                    <div class="alert alert-danger alert-dismissable">
                        <button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>
                        <?php echo $this->session->flashdata('error'); ?>
                    </div>
                <?php } ?>
                <?php
                $success = $this->session->flashdata('success');
                if($success)
                {
                    ?>
                    <div class="alert alert-success alert-dismissable">
                        <button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>
                        <?php echo $this->session->flashdata('success'); ?>
                    </div>
                <?php } ?>

                <?php
                $noMatch = $this->session->flashdata('nomatch');
                if($noMatch)
                {
                    ?>
                    <div class="alert alert-warning alert-dismissable">
                        <button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>
                        <?php echo $this->session->flashdata('nomatch'); ?>
                    </div>
                <?php } ?>

                <div class="row">
                    <div class="col-md-12">
                        <?php echo validation_errors('<div class="alert alert-danger alert-dismissable">', ' <button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button></div>'); ?>
                    </div>
                </div>
            </div>
        </div>
    </section>
</div>

<script src="<?php echo base_url(); ?>assets/js/editUser.js" type="text/javascript"></script>