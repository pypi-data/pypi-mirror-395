import requests
import cv2
import numpy as np
import csv
import os
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class KSface:
    """KSfaceAPI主类 - 提供简单的人脸识别接口"""
    
    def __init__(self, api_key=None, api_secret=None, faceset_id="shisai", csv_filename="face_tokens.csv"):
        """
        初始化KSfaceAPI
        
        Args:
            api_key: Face++ API Key
            api_secret: Face++ API Secret
            faceset_id: 人脸库ID，默认"shisai"
            csv_filename: CSV文件名，默认在当前目录生成
        """
        self.API_KEY = api_key or "empen2tifVJNcJ1b4-_BGJcHEQGomqp-"
        self.API_SECRET = api_secret or "MKZN4H02uBB7KvAsiHB7O3x1g6zPRqq1"
        self.FACESET_ID = faceset_id
        
        # API URLs
        self.DETECT_URL = "https://api-cn.faceplusplus.com/facepp/v3/detect"
        self.CREATE_FACESET_URL = "https://api-cn.faceplusplus.com/facepp/v3/faceset/create"
        self.ADD_FACE_URL = "https://api-cn.faceplusplus.com/facepp/v3/faceset/addface"
        self.SEARCH_FACE_URL = "https://api-cn.faceplusplus.com/facepp/v3/search"
        self.REMOVE_FACE_URL = "https://api-cn.faceplusplus.com/facepp/v3/faceset/removeface"
        
        # CSV文件路径 - 使用调用脚本的当前目录
        self.CSV_FILE = csv_filename
        
        # 加载现有映射
        self._load_map()
    
    def _load_map(self):
        """加载人脸映射关系"""
        self.face_map = {}
        if not os.path.exists(self.CSV_FILE):
            logger.info(f"CSV file {self.CSV_FILE} not found, will create new")
            return
        
        try:
            with open(self.CSV_FILE, mode='r', encoding='utf-8', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.face_map[row['face_token']] = row['face_id']
            logger.info(f"Loaded {len(self.face_map)} face mappings from {self.CSV_FILE}")
        except Exception as e:
            logger.error(f"Failed to load CSV: {str(e)}")
    
    def _save_map(self):
        """保存所有人脸映射关系到CSV"""
        try:
            with open(self.CSV_FILE, mode='w', encoding='utf-8', newline='') as file:
                fieldnames = ['face_token', 'face_id']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for token, fid in self.face_map.items():
                    writer.writerow({'face_token': token, 'face_id': fid})
            return True
        except Exception as e:
            logger.error(f"Failed to save CSV: {str(e)}")
            return False
    
    def _get_id(self, face_token):
        """根据token获取编号"""
        return self.face_map.get(face_token, "unknown")
    
    def _get_token(self, face_id):
        """根据编号获取token"""
        for token, fid in self.face_map.items():
            if fid == face_id:
                return token
        return None
    
    def create(self):
        """创建人脸库"""
        params = {
            "api_key": self.API_KEY,
            "api_secret": self.API_SECRET,
            "outer_id": self.FACESET_ID
        }
        try:
            response = requests.post(self.CREATE_FACESET_URL, data=params)
            result = response.json()
            if "error_message" in result:
                logger.error(f"Create failed: {result['error_message']}")
                return False
            else:
                logger.info(f"Faceset created: {result['outer_id']}")
                return True
        except Exception as e:
            logger.error(f"Network error: {str(e)}")
            return False
    
    def add(self, image_path, face_id):
        """
        添加人脸
        
        Args:
            image_path: 图片路径
            face_id: 人脸编号
            
        Returns:
            bool: 是否成功
        """
        # 检测人脸
        try:
            with open(image_path, "rb") as f:
                files = {"image_file": f}
                detect_params = {
                    "api_key": self.API_KEY,
                    "api_secret": self.API_SECRET,
                    "return_landmark": 0
                }
                detect_response = requests.post(self.DETECT_URL, data=detect_params, files=files)
                detect_result = detect_response.json()
            
            if "error_message" in detect_result:
                logger.error(f"Face detection failed: {detect_result['error_message']}")
                return False
            if not detect_result.get("faces"):
                logger.error("No face detected")
                return False
            
            face_token = detect_result["faces"][0]["face_token"]
            
            # 添加到人脸库
            add_params = {
                "api_key": self.API_KEY,
                "api_secret": self.API_SECRET,
                "outer_id": self.FACESET_ID,
                "face_tokens": face_token
            }
            add_response = requests.post(self.ADD_FACE_URL, data=add_params)
            add_result = add_response.json()

            if "error_message" in add_result:
                logger.error(f"Add face failed: {add_result['error_message']}")
                return False
            else:
                # 保存映射
                self.face_map[face_token] = face_id
                self._save_map()
                logger.info(f"Face added: {face_id}")
                return True
        
        except FileNotFoundError:
            logger.error(f"Image not found: {image_path}")
            return False
        except Exception as e:
            logger.error(f"Add face error: {str(e)}")
            return False
    
    def find(self, image_source):
        """
        查找人脸
        
        Args:
            image_source: 图片路径或numpy数组(frame)
            
        Returns:
            str: 人员编号，如果未找到返回None
        """
        try:
            if isinstance(image_source, str):
                # 文件路径
                with open(image_source, "rb") as f:
                    files = {"image_file": f}
                    result = self._search(files)
            else:
                # numpy数组 (摄像头帧)
                rgb_frame = cv2.cvtColor(image_source, cv2.COLOR_BGR2RGB)
                success, encoded_image = cv2.imencode('.jpg', rgb_frame)
                if not success:
                    return None
                image_bytes = encoded_image.tobytes()
                files = {"image_file": image_bytes}
                result = self._search(files)
            
            return result["id"] if result else None
        
        except Exception as e:
            logger.error(f"Search error: {str(e)}")
            return None
    
    def _search(self, files):
        """执行搜索"""
        search_params = {
            "api_key": self.API_KEY,
            "api_secret": self.API_SECRET,
            "outer_id": self.FACESET_ID,
            "return_result_count": 1
        }
        
        search_response = requests.post(self.SEARCH_FACE_URL, data=search_params, files=files)
        search_result = search_response.json()
        
        if "error_message" in search_result:
            logger.error(f"Search failed: {search_result['error_message']}")
            return None
        
        if not search_result.get("results"):
            return None
        
        # 处理结果
        best_match = search_result["results"][0]
        face_id = self._get_id(best_match['face_token'])
        
        return {
            "id": face_id,
            "confidence": best_match['confidence'],
            "token": best_match['face_token']
        }
    
    def remove(self, face_identifier):
        """
        删除人脸
        
        Args:
            face_identifier: 人脸编号或token
            
        Returns:
            bool: 是否成功
        """
        # 判断输入类型
        face_token = None
        if len(face_identifier) < 20:  # 编号
            face_token = self._get_token(face_identifier)
            if not face_token:
                logger.error(f"Face ID not found: {face_identifier}")
                return False
        else:  # token
            face_token = face_identifier
        
        # 调用删除API
        params = {
            "api_key": self.API_KEY,
            "api_secret": self.API_SECRET,
            "outer_id": self.FACESET_ID,
            "face_tokens": face_token
        }
        
        try:
            response = requests.post(self.REMOVE_FACE_URL, data=params)
            result = response.json()
            
            if "error_message" in result:
                logger.error(f"Remove failed: {result['error_message']}")
                return False
            else:
                # 从映射中删除
                if face_token in self.face_map:
                    del self.face_map[face_token]
                    self._save_map()
                logger.info(f"Face removed: {face_token}")
                return True
        
        except Exception as e:
            logger.error(f"Remove error: {str(e)}")
            return False
    
    def clear(self):
        """清空人脸库"""
        params = {
            "api_key": self.API_KEY,
            "api_secret": self.API_SECRET,
            "outer_id": self.FACESET_ID,
            "face_tokens": "RemoveAllFaceTokens"
        }
        
        try:
            response = requests.post(self.REMOVE_FACE_URL, data=params)
            result = response.json()
            
            if "error_message" in result:
                logger.error(f"Clear failed: {result['error_message']}")
                return False
            else:
                # 清空映射
                self.face_map.clear()
                self._save_map()
                logger.info("All faces cleared")
                return True
        
        except Exception as e:
            logger.error(f"Clear error: {str(e)}")
            return False
    
    def list(self):
        """列出所有人脸映射"""
        return self.face_map.copy()