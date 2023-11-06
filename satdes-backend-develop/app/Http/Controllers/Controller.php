<?php

namespace App\Http\Controllers;

use Illuminate\Http\Response;
use Illuminate\Foundation\Auth\Access\AuthorizesRequests;
use Illuminate\Foundation\Validation\ValidatesRequests;
use Illuminate\Routing\Controller as BaseController;

class Controller extends BaseController
{
    use AuthorizesRequests, ValidatesRequests;
  
    /**
     * Return a Success JSON Response with data
     *
     * @param string  $message
     * @param mixed   $data
     * @param integer $status
     * 
     * @return \Illuminate\Http\Response
     */
    protected function successResponse($message = 'Success', $status = 200, $data = null)
    {
        return response()->json([
            'success' => true,
            'message' => $message,
            'data'    => $data,
        ], $status);
    }
    
    /**
     * Return a Error JSON Response with message
     *
     * @param string  $message
     * @param integer $status
     * @param mixed   $data
     * 
     * @return \Illuminate\Http\Response
     */
    protected function errorResponse($message = 'Error', $status = 400, $data = null)
    {
        return response()->json([
            'success' => false,
            'message' => $message,
            'data'    => $data,
        ], $status);
    }
}
