import json
import logging
import base64
from typing import Dict, Any, List
from tornado.web import RequestHandler
from tornado.escape import json_decode

from services import (
    BiddingProductService,
    WinningProductService,
    CodeExtractionService,
    DistrictTimeService,
    NoticeTypeService,
    BidTypeService,
    ContactInfoService,
    MultimodalService
)

class TextServiceHandler(RequestHandler):
    """文本服务处理器"""
    
    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # 初始化所有文本服务
        self.services = {
            'bidding_product': BiddingProductService(),
            'winning_product': WinningProductService(),
            'code_extraction': CodeExtractionService(),
            'district_time': DistrictTimeService(),
            'notice_type': NoticeTypeService(),
            'bid_type': BidTypeService(),
            'contact_info': ContactInfoService()
        }
    
    def post(self):
        """处理文本服务请求"""
        try:
            # 解析请求数据
            request_data = json_decode(self.request.body)
            
            # 验证必需参数
            required_fields = ['service_type', 'notice_id', 'content']
            for field in required_fields:
                if field not in request_data:
                    self.set_status(400)
                    self.write({
                        'success': False,
                        'error': f'Missing required field: {field}'
                    })
                    return
            
            service_type = request_data['service_type']
            notice_id = request_data['notice_id']
            content = request_data['content']
            extra_info = request_data.get('extra_info', {})
            
            # 验证服务类型
            if service_type not in self.services:
                self.set_status(400)
                self.write({
                    'success': False,
                    'error': f'Unsupported service type: {service_type}'
                })
                return
            
            # 调用对应的服务
            service = self.services[service_type]
            result = service.process(notice_id, content, extra_info)
            
            # 返回结果
            self.set_header('Content-Type', 'application/json')
            self.write(result)
            
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON decode error: {str(e)}")
            self.set_status(400)
            self.write({
                'success': False,
                'error': 'Invalid JSON format'
            })
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            self.set_status(500)
            self.write({
                'success': False,
                'error': 'Internal server error'
            })

class MultimodalServiceHandler(RequestHandler):
    """多模态服务处理器"""
    
    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.multimodal_service = MultimodalService()
    
    def post(self):
        """处理多模态服务请求"""
        try:
            # 检查请求类型
            content_type = self.request.headers.get('Content-Type', '')
            
            if 'multipart/form-data' in content_type:
                # 处理文件上传
                self._handle_file_upload()
            else:
                # 处理JSON请求
                self._handle_json_request()
                
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            self.set_status(500)
            self.write({
                'success': False,
                'error': 'Internal server error'
            })
    
    def _handle_file_upload(self):
        """处理文件上传请求"""
        try:
            # 获取表单数据
            notice_id = self.get_argument('notice_id', None)
            extra_info_str = self.get_argument('extra_info', '{}')
            
            if not notice_id:
                self.set_status(400)
                self.write({
                    'success': False,
                    'error': 'Missing notice_id'
                })
                return
            
            # 解析extra_info
            try:
                extra_info = json.loads(extra_info_str) if extra_info_str else {}
            except json.JSONDecodeError:
                extra_info = {}
            
            # 获取上传的文件
            files = self.request.files
            if not files:
                self.set_status(400)
                self.write({
                    'success': False,
                    'error': 'No files uploaded'
                })
                return
            
            # 处理文件
            pdf_files = []
            image_files = []
            
            for field_name, file_list in files.items():
                for file_info in file_list:
                    filename = file_info['filename']
                    file_data = file_info['body']
                    
                    # 根据文件类型分类
                    if filename.lower().endswith('.pdf'):
                        pdf_files.append(file_data)
                    elif any(filename.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg']):
                        image_files.append(file_data)
            
            # 调用相应的处理方法
            if pdf_files:
                if len(pdf_files) > 1:
                    self.set_status(400)
                    self.write({
                        'success': False,
                        'error': 'Only one PDF file is allowed per request'
                    })
                    return
                
                result = self.multimodal_service.process_pdf(notice_id, pdf_files[0], extra_info)
            elif image_files:
                result = self.multimodal_service.process_images(notice_id, image_files, extra_info)
            else:
                self.set_status(400)
                self.write({
                    'success': False,
                    'error': 'No supported files found'
                })
                return
            
            # 返回结果
            self.set_header('Content-Type', 'application/json')
            self.write(result)
            
        except Exception as e:
            self.logger.error(f"File upload error: {str(e)}")
            self.set_status(500)
            self.write({
                'success': False,
                'error': 'File processing error'
            })
    
    def _handle_json_request(self):
        """处理JSON请求（用于base64编码的文件数据）"""
        try:
            request_data = json_decode(self.request.body)
            
            # 验证必需参数
            required_fields = ['notice_id', 'file_type']
            for field in required_fields:
                if field not in request_data:
                    self.set_status(400)
                    self.write({
                        'success': False,
                        'error': f'Missing required field: {field}'
                    })
                    return
            
            notice_id = request_data['notice_id']
            file_type = request_data['file_type']
            extra_info = request_data.get('extra_info', {})
            
            if file_type == 'pdf':
                # 处理PDF文件
                if 'file_data' not in request_data:
                    self.set_status(400)
                    self.write({
                        'success': False,
                        'error': 'Missing file_data for PDF'
                    })
                    return
                
                try:
                    pdf_data = base64.b64decode(request_data['file_data'])
                    result = self.multimodal_service.process_pdf(notice_id, pdf_data, extra_info)
                except Exception as e:
                    self.set_status(400)
                    self.write({
                        'success': False,
                        'error': f'Invalid PDF data: {str(e)}'
                    })
                    return
                    
            elif file_type == 'images':
                # 处理图片文件
                if 'file_data_list' not in request_data:
                    self.set_status(400)
                    self.write({
                        'success': False,
                        'error': 'Missing file_data_list for images'
                    })
                    return
                
                try:
                    image_files = []
                    for file_data_b64 in request_data['file_data_list']:
                        image_data = base64.b64decode(file_data_b64)
                        image_files.append(image_data)
                    
                    result = self.multimodal_service.process_images(notice_id, image_files, extra_info)
                except Exception as e:
                    self.set_status(400)
                    self.write({
                        'success': False,
                        'error': f'Invalid image data: {str(e)}'
                    })
                    return
            else:
                self.set_status(400)
                self.write({
                    'success': False,
                    'error': f'Unsupported file type: {file_type}'
                })
                return
            
            # 返回结果
            self.set_header('Content-Type', 'application/json')
            self.write(result)
            
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON decode error: {str(e)}")
            self.set_status(400)
            self.write({
                'success': False,
                'error': 'Invalid JSON format'
            })

class HealthCheckHandler(RequestHandler):
    """健康检查处理器"""
    
    def get(self):
        """健康检查接口"""
        self.write({
            'status': 'healthy',
            'service': 'huayu_service_engine',
            'version': '1.0.0'
        }) 