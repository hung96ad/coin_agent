<div class="content-wrapper">
    <!-- Content Header (Page header) -->
    <section class="content-header">
      <h1>
        <i class="fa fa-users"></i> Home page Management
        <small>Add, Edit, Delete</small>
      </h1>
    </section>
    <section class="content">
        <div class="row">
            <div class="col-xs-12 text-right">
                <div class="form-group">
                    <a class="btn btn-primary" href="<?php echo base_url(); ?>addWallet"><i class="fa fa-plus"></i> Add wallet</a>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-xs-12">
              <div class="box">
                <div class="box-header">
                    <h3 class="box-title">Home page List</h3>
                </div><!-- /.box-header -->
                <div class="box-body table-responsive no-padding">
                  <table class="table table-hover">
                    <tr>
                        <th>Title</th>
                        <th>Email</th>
                        <th>Name wallet</th>
                        <th>Wallet address</th>
                        <th class="text-center">Actions</th>
                    </tr>
                    <?php
                    if(!empty($configIndex))
                    {
                        foreach($configIndex as $record)
                        {
                    ?>
                    <tr>
                        <td><?php echo $record->title ?></td>
                        <td><?php echo $record->email ?></td>
                        <td><?php echo $record->name ?></td>
                        <td><?php echo $record->wallet ?></td>
                        <td class="text-center">
                            <a class="btn btn-sm btn-primary" href="<?= base_url().'editTitleOld/'.$record->id; ?>" title="Edit home page, title"><i class="fa fa-pencil"> Edit title, email</i></a> | 
                            <a class="btn btn-sm btn-info" href="<?php echo base_url().'editWallet/'.$record->name; ?>" title="Edit wallet"><i class="fa fa-pencil"></i></a>
                            <a class="btn btn-sm btn-danger deleteWallet" href="#" data-wallet="<?php echo $record->name; ?>" title="Delete"><i class="fa fa-trash"></i></a>
                        </td>
                    </tr>
                    <?php
                        }
                    }
                    ?>
                  </table>
                  
                </div><!-- /.box-body -->
                <div class="box-footer clearfix">
                </div>
              </div><!-- /.box -->
            </div>
        </div>
    </section>
</div>
<script type="text/javascript" src="<?php echo base_url(); ?>assets/js/common_wallet.js?id1" charset="utf-8"></script>
