// KintctDLL.cpp : DLL 응용 프로그램을 위해 내보낸 함수를 정의합니다.
//

#include "stdafx.h"
#include "testkinect.h"
#include "KinectAPI.h"
#include "BlobLabeling.h"

CBlobLabeling blob;

namespace TestKinect{
	mKinect::mKinect() :m_nStartTime(0),
		m_nLastCounter(0),
		m_nFramesSinceUpdate(0),
		m_fFreq(0),
		m_nNextStatusTime(0LL),
		m_bSaveScreenshot(false),
		m_pKinectSensor(NULL),
		m_pCoordinateMapper(NULL),
		m_pMultiSourceFrameReader(NULL),
		m_pDepthCoordinates(NULL),
		m_pOutputRGBX(NULL),
		m_pBackgroundRGBX(NULL),
		m_pColorRGBX(NULL)
	{
		std::cout << "kinect ctor" << std::endl;
		mColorMat = cv::Mat(cColorHeight, cColorWidth, CV_8UC4);
		mDepthBufferMat = cv::Mat(cDepthHeight, cDepthWidth, CV_16UC1);
		mDepthMat = cv::Mat(cDepthHeight, cDepthWidth, CV_8UC1);
		mCoordinateMat = cv::Mat(cDepthHeight,cDepthWidth,CV_8UC4);

		// create heap storage for composite image pixel data in RGBX format
		m_pOutputRGBX = new RGBQUAD[cColorWidth * cColorHeight];

		// create heap storage for background image pixel data in RGBX format
		m_pBackgroundRGBX = new RGBQUAD[cColorWidth * cColorHeight];

		// create heap storage for color pixel data in RGBX format
		m_pColorRGBX = new RGBQUAD[cColorWidth * cColorHeight];

		// create heap storage for the coorinate mapping from color to depth
		m_pDepthCoordinates = new DepthSpacePoint[cColorWidth * cColorHeight];

		depthBuffer = new UINT16[cDepthHeight * cDepthWidth];
	}

	mKinect::~mKinect(){
		std::cout << "kinect dtor" << std::endl; 

		if (m_pOutputRGBX)
		{
			delete[] m_pOutputRGBX;
			m_pOutputRGBX = NULL;
		}

		if (m_pBackgroundRGBX)
		{
			delete[] m_pBackgroundRGBX;
			m_pBackgroundRGBX = NULL;
		}

		if (m_pColorRGBX)
		{
			delete[] m_pColorRGBX;
			m_pColorRGBX = NULL;
		}

		if (m_pDepthCoordinates)
		{
			delete[] m_pDepthCoordinates;
			m_pDepthCoordinates = NULL;
		}

		// done with frame reader
		SafeRelease(m_pMultiSourceFrameReader);

		// done with coordinate mapper
		SafeRelease(m_pCoordinateMapper);

		// close the Kinect Sensor
		if (m_pKinectSensor)
		{
			m_pKinectSensor->Close();
		}

		SafeRelease(m_pKinectSensor);
	}

	void mKinect::initialize(){

	}

	void mKinect::Finalize(){

	}

	void mKinect::get(int& a, float& b){
		a = m_a;
		b = m_b;
	}

	void mKinect::set(int a, float b){
		m_a = a;
		m_b = b;
	}

	void mKinect::print(){
		//std::cout << "val a = " << m_a << " val b = " << m_b << std::endl;
		cv::imshow("image", mDepthMat);
		if (cv::waitKey(30) == VK_ESCAPE){
			return;
		}
	}

	int* mKinect::getContourLen(){
		return contours_len;
	}

	int mKinect::mockupLoadimage(const char*imagePath){
		shadowImage = cv::imread(imagePath);
		return 1;
	}

	POINT** mKinect::getContours(){
		POINT**mlist = new POINT*[contours.size()];
		for (int i = 0; i < contours_size; ++i){
			mlist[i] = new POINT[contours[i].size()];
			for (int j = 0; j < contours[i].size(); ++j){
				mlist[i][j].x = contours[i][j].x;
				mlist[i][j].y = contours[i][j].y;
			}
		}
		return mlist;
	}

	POINT* mKinect::getContourCenter(){
		POINT* mlist = new POINT[contours.size()];

		contours_len = new int[contours_size];

		for (int i = 0; i < contours.size(); ++i){

			int x = 0;
			int y = 0;

			for (int j = 0; j < contours[i].size(); ++j){
				x += contours[i][j].x;
				y += contours[i][j].y;
			}

			x /= contours[i].size();
			y /= contours[i].size();

			mlist[i].x = x;
			mlist[i].y = y;

			contours_len[i] = contours[i].size();

		}
		return mlist;
	}

	void mKinect::updateContour(){
		cv::Mat grayMat(shadowImage.rows, shadowImage.cols, CV_8UC3);
		std::cout << "grayMat create" << std::endl;
		cv::Mat cannyMat(shadowImage.rows, shadowImage.cols, CV_8UC3);
		std::cout << "cannyMat create" << std::endl;
		cv::cvtColor(shadowImage, grayMat, CV_RGB2GRAY);
		std::cout << "gray convert" << std::endl;
		cv::Canny(grayMat, cannyMat, 30, 128, 3, false); // contour 찾기위한 cannyedge 작업
		std::cout << "canny convert" << std::endl;
		cv::findContours(cannyMat, contours, cv::RETR_EXTERNAL, cv::CHAIN_APPROX_SIMPLE); // contour 찾기
		std::cout << "findcontours " << contours.size() << std::endl;
		contours_size = contours.size();
		std::cout << "set contours size " << contours_size << std::endl;
	}

	unsigned char* mKinect::getShadowImage(){
		return shadowImage.data;
	}

	POINT**mKinect::getTouchList(bool touch){
		if (touch){

			POINT**mlist = new POINT*[true_touchcontours.size()];
			for (int i = 0; i < true_touchcontours.size(); ++i){
				mlist[i] = new POINT[true_touchcontours[i].size()];
				for (int j = 0; j < true_touchcontours[i].size(); ++j){
					mlist[i][j].x = true_touchcontours[i][j].x;
					mlist[i][j].y = true_touchcontours[i][j].y;
				}
			}
			return mlist;
		}
		else{

			POINT**mlist = new POINT*[false_touchcontours.size()];
			for (int i = 0; i < false_touchcontours.size(); ++i){
				mlist[i] = new POINT[false_touchcontours[i].size()];
				for (int j = 0; j < false_touchcontours[i].size(); ++j){
					mlist[i][j].x = false_touchcontours[i][j].x;
					mlist[i][j].y = false_touchcontours[i][j].y;
				}
			}
			return mlist;
		}
	}
	int*mKinect::getTouchContourLen(bool touch){
		if (touch){
			int*len = new int[true_touchcontours.size()];

			for (int i = 0; i < true_touchcontours.size(); ++i){
				len[i] = true_touchcontours[i].size();
			}

			return len;
		}
		else{
			int*len = new int[false_touchcontours.size()];

			for (int i = 0; i < false_touchcontours.size(); ++i){
				len[i] = false_touchcontours[i].size();
			}
			return len;
		}
	}
	int mKinect::getTouchContoursSize(bool touch){
		if (touch){
			return true_touchcontours.size();
		}
		else{
			return false_touchcontours.size();
		}
	}

	int mKinect::touchmockupLoadimage(const char* name, bool touch){
		if (touch){
			true_touchPoint = cv::imread(name);
		}
		else{
			false_touchPoint = cv::imread(name);
		}
		return 1;
	}

	void mKinect::updateTouchContour(){
		cv::Mat grayMat(true_touchPoint.rows, true_touchPoint.cols, CV_8UC3);
		std::cout << "grayMat create" << std::endl;
		cv::Mat cannyMat(true_touchPoint.rows, true_touchPoint.cols, CV_8UC3);
		std::cout << "cannyMat create" << std::endl;
		cv::cvtColor(true_touchPoint, grayMat, CV_RGB2GRAY);
		std::cout << "gray convert" << std::endl;
		cv::Canny(grayMat, cannyMat, 30, 128, 3, false); // contour 찾기위한 cannyedge 작업
		std::cout << "canny convert" << std::endl;
		cv::findContours(cannyMat, true_touchcontours, cv::RETR_EXTERNAL, cv::CHAIN_APPROX_SIMPLE); // contour 찾기
		std::cout << "findcontours " << true_touchcontours.size() << std::endl;
		//contours_size = contours.size();
		//std::cout << "set contours size " << contours_size << std::endl;

		cv::Mat grayMat1(false_touchPoint.rows, false_touchPoint.cols, CV_8UC3);
		std::cout << "grayMat1 create" << std::endl;
		cv::Mat cannyMat1(false_touchPoint.rows, false_touchPoint.cols, CV_8UC3);
		std::cout << "cannyMat1 create" << std::endl;
		cv::cvtColor(false_touchPoint, grayMat1, CV_RGB2GRAY);
		std::cout << "gray convert" << std::endl;
		cv::Canny(grayMat1, cannyMat1, 30, 128, 3, false); // contour 찾기위한 cannyedge 작업
		std::cout << "canny convert" << std::endl;
		cv::findContours(cannyMat1, false_touchcontours, cv::RETR_EXTERNAL, cv::CHAIN_APPROX_SIMPLE); // contour 찾기
		std::cout << "findcontours " << false_touchcontours.size() << std::endl;
	}

	int mKinect::createShadowImage(){ // 이미지 만들기 부분. 이미지를 만들어 png로 저장한다. 만들어진 이미지의 개수를 넘겨준다.
		int count = 0;

		return count;
	}

	POINT** mKinect::getImageContours(int num){
		POINT** list = nullptr;
		
		return list;
	}
	POINT* mKinect::getImageContoursCenter(int num){
		POINT* list = nullptr;

		cv::Mat cannyMat(cDepthHeight, cDepthWidth, CV_8UC1);
		cv::Canny(mDepthMat, cannyMat, 30, 128, 3, false); // contour 찾기위한 cannyedge 작업
		cv::findContours(cannyMat, contours, cv::RETR_EXTERNAL, cv::CHAIN_APPROX_SIMPLE); // contour 찾기
		//cv::drawContours(tempMat, contours, -1, cv::Scalar(0, 0, 255), 1);				  // contour 그리기
		
		list = new POINT[contours.size()];

		for (int i = 0; i < contours.size(); ++i){
			for (int j = 0; j < contours[i].size(); ++j){
				list[i].x += contours[i][j].x;
				list[i].y += contours[i][j].y;
			}
			list[i].x = list[i].x / contours[i].size();
			list[i].y = list[i].y / contours[i].size();
		}

		return list;
	}
	POINT** mKinect::getTouchContours(){
		POINT** list = nullptr;
		
		return list;
	}
	HRESULT mKinect::InitKinect(){ // 키넥트 초기화!!!
		HRESULT hr;

		hr = GetDefaultKinectSensor(&m_pKinectSensor);
		if (FAILED(hr)){
			return hr;
		}

		if (m_pKinectSensor){
			if (SUCCEEDED(hr)){
				hr = m_pKinectSensor->get_CoordinateMapper(&m_pCoordinateMapper);
			}

			hr = m_pKinectSensor->Open();

			if (SUCCEEDED(hr)){
				hr = m_pKinectSensor->OpenMultiSourceFrameReader(FrameSourceTypes::FrameSourceTypes_Depth | FrameSourceTypes::FrameSourceTypes_Color | FrameSourceTypes::FrameSourceTypes_BodyIndex,
					&m_pMultiSourceFrameReader);
			}
		}
		if (!m_pKinectSensor || FAILED(hr)){
			return E_FAIL;
		}

		return hr; // S_OK return
	}

	void mKinect::ProcessFrame(INT64 nTime,const UINT16* pDepthBuffer, int nDepthWidth, int nDepthHeight,const RGBQUAD* pColorBuffer, int nColorWidth, int nColorHeight,const BYTE* pBodyIndexBuffer, int nBodyIndexWidth, int nBodyIndexHeight){
		const RGBQUAD c_green = { 255, 255, 255, 0 };
		
		// Fill in with a background colour of green if we can't load the background image
		for (int i = 0; i < cColorWidth * cColorHeight; ++i)
		{
			m_pBackgroundRGBX[i] = c_green;
		}
		
		std::cout << "process frame" << std::endl;
		int count = 1;
		std::cout << count++ << " 1process" << std::endl;
		// Make sure we've received valid data
		if (m_pCoordinateMapper && m_pDepthCoordinates && m_pOutputRGBX &&
			pDepthBuffer && (nDepthWidth == cDepthWidth) && (nDepthHeight == cDepthHeight) &&
			pColorBuffer && (nColorWidth == cColorWidth) && (nColorHeight == cColorHeight) &&
			pBodyIndexBuffer && (nBodyIndexWidth == cDepthWidth) && (nBodyIndexHeight == cDepthHeight))
		{
			std::cout << count++ << " 2process" << std::endl;
			HRESULT hr = m_pCoordinateMapper->MapColorFrameToDepthSpace(nDepthWidth * nDepthHeight, (UINT16*)pDepthBuffer, nColorWidth * nColorHeight, m_pDepthCoordinates);
			if (SUCCEEDED(hr))
			{
				std::cout << count++ << " 3process" << std::endl;
				const RGBQUAD shadow = { 0, 0, 0, 255 };
				// loop over output pixels
				for (int colorIndex = 0; colorIndex < (nColorWidth*nColorHeight); ++colorIndex)
				{
					// default setting source to copy from the background pixel
					const RGBQUAD* pSrc = m_pBackgroundRGBX + colorIndex;

					DepthSpacePoint p = m_pDepthCoordinates[colorIndex];

					// Values that are negative infinity means it is an invalid color to depth mapping so we
					// skip processing for this pixel
					if (p.X != -std::numeric_limits<float>::infinity() && p.Y != -std::numeric_limits<float>::infinity())
					{
						int depthX = static_cast<int>(p.X + 0.5f);
						int depthY = static_cast<int>(p.Y + 0.5f);

						if ((depthX >= 0 && depthX < nDepthWidth) && (depthY >= 0 && depthY < nDepthHeight))
						{
							BYTE player = pBodyIndexBuffer[depthX + (depthY * cDepthWidth)];

							// if we're tracking a player for the current pixel, draw from the color camera
							if (player != 0xff)
							{
								// set source for copy to the color pixel
								//pSrc = m_pColorRGBX + colorIndex;
								pSrc = &shadow;
							}
						}
					}

					// write output
					m_pOutputRGBX[colorIndex] = *pSrc;
				}
				cv::Mat img(cColorHeight, cColorWidth, CV_8UC4,
					reinterpret_cast<void*>(m_pOutputRGBX));
				mColorMat = img.clone();
				std::cout << count++ << " 4process" << std::endl;

				cv::Mat mat;// = mColorMat.clone();
				
				mat = mColorMat.clone();
				cv::flip(mColorMat, mat, 1);
				cv::medianBlur(mat, mat, 3);
				
				cv::Mat label(mat.rows, mat.cols, CV_8UC1);
				cv::Mat whitemat = ~mat.clone();

				cv::cvtColor(whitemat, label, CV_BGR2GRAY);

				IplImage* labelImage = new IplImage(label);
				blob.SetParam(labelImage, 200);
				blob.DoLabeling();
				blob.BlobSmallSizeConstraint(70, 70);

				CvRect*rect = blob.m_recBlobs;
				//std::cout << "start labeling   " << blob.m_nBlobs << std::endl;
				imagecount = blob.m_nBlobs;
				for (int i = 0; i < blob.m_nBlobs; ++i){
					cv::Rect mrect;// = rect[i];
					mrect.x = rect[i].x;
					mrect.y = rect[i].y;
					mrect.width = rect[i].width;
					mrect.height = rect[i].height;
					//std::cout << "width: " << mrect.width << " height: " << mrect.height << " x: " << mrect.x << " y:" << mrect.y << std::endl;
					//mat()
					cv::Mat saveImage;
					mat(mrect).copyTo(saveImage);

					std::vector<int> compression_params;
					compression_params.push_back(CV_IMWRITE_PNG_COMPRESSION);
					compression_params.push_back(9);

					char buf[20];

					sprintf_s(buf, "picture%d.png", i);

					//std::cout << buf << " create" << std::endl;

					try {
						imwrite(buf, saveImage, compression_params);
					}
					catch (std::runtime_error& ex) {
						fprintf(stderr, "Exception converting image to PNG format: %s\n", ex.what());
						return;
					}
				}
				/*std::vector<int> compression_params;
				compression_params.push_back(CV_IMWRITE_PNG_COMPRESSION);
				compression_params.push_back(9);

				char buf[20];

				sprintf_s(buf, "picture%d.png", 3);

				try {
					imwrite(buf, mat, compression_params);
				}
				catch (std::runtime_error& ex) {
					fprintf(stderr, "Exception converting image to PNG format: %s\n", ex.what());
					return;
				}*/
			

			}
		}

	}

	void mKinect::processIncomingData() {
		
		if (!m_pMultiSourceFrameReader)
		{
			return;
		}

		if (depthBuffer != nullptr) {
			delete[] depthBuffer;
			depthBuffer = nullptr;
		}

		IMultiSourceFrame* pMultiSourceFrame = NULL;
		IDepthFrame* data = NULL;
		IFrameDescription *frameDesc = nullptr;

		HRESULT hr = m_pMultiSourceFrameReader->AcquireLatestFrame(&pMultiSourceFrame);
		//std::cout << count++ << " 4번째" << std::endl;
		if (SUCCEEDED(hr)){
			IDepthFrameReference*pDepthFrameReference = NULL;
			//std::cout << hr << "1오류임" << std::endl;
			hr = pMultiSourceFrame->get_DepthFrameReference(&pDepthFrameReference);
			if (SUCCEEDED(hr)){
				//std::cout << hr << "2오류임" << std::endl;
				hr = pDepthFrameReference->AcquireFrame(&data);
			}
			SafeRelease(pDepthFrameReference);
		}

		//IDepthFrame *data = nullptr;
		//HRESULT hr = -1;
		
		USHORT nDepthMinReliableDistance = 0;
		USHORT nDepthMaxReliableDistance = 0;
		int height = 424, width = 512;
		std::cout << "depth 1" << std::endl;
		if (SUCCEEDED(hr)) hr = data->get_FrameDescription(&frameDesc);
		std::cout << "depth 2" << std::endl;
		if (SUCCEEDED(hr)) hr = data->get_DepthMinReliableDistance(
			&nDepthMinReliableDistance);
		std::cout << "depth 3" << std::endl;
		if (SUCCEEDED(hr)) hr = data->get_DepthMaxReliableDistance(
			&nDepthMaxReliableDistance);
		std::cout << "depth 4" << std::endl;
		if (SUCCEEDED(hr)) {
			std::cout << "depth 5" << std::endl;
			if (SUCCEEDED(frameDesc->get_Height(&height)) &&
				SUCCEEDED(frameDesc->get_Width(&width))) {
				std::cout << "depth 6" << std::endl;
				hr = data->CopyFrameDataToArray(cDepthHeight * cDepthWidth, depthBuffer);
				if (SUCCEEDED(hr)) {
					std::cout << "depth 7" << std::endl;
					cv::Mat depthMap = cv::Mat(height, width, CV_16U, depthBuffer);
					cv::Mat img0 = cv::Mat::zeros(height, width, CV_8UC1);
					cv::Mat img1;
					double scale = 255.0 / (nDepthMaxReliableDistance -
						nDepthMinReliableDistance);
					depthMap.convertTo(img0, CV_8UC1, scale);
					//cv::applyColorMap(img0, img1, cv::COLORMAP_JET);
					//cv::imshow("Depth Only", img1);
					mDepthMat = img0.clone();
				}
			}
		}
		SafeRelease(data);
		
	}

	long mKinect::getLen(){
		return contours.size();
	}

	void mKinect::getDepthImage(){
		if (!m_pMultiSourceFrameReader)
		{
			std::cout << "multisourceFrameReader nullptr" << std::endl;
			return ;
		}
		IMultiSourceFrame* pMultiSourceFrame = NULL;
		IDepthFrame* pDepthFrame = NULL;

		HRESULT hr = m_pMultiSourceFrameReader->AcquireLatestFrame(&pMultiSourceFrame);

		if (SUCCEEDED(hr)){
			IDepthFrameReference*pDepthFrameReference = NULL;
			//std::cout << hr << "1오류임" << std::endl;
			hr = pMultiSourceFrame->get_DepthFrameReference(&pDepthFrameReference);
			if (SUCCEEDED(hr)){
				//std::cout << hr << "2오류임" << std::endl;
				hr = pDepthFrameReference->AcquireFrame(&pDepthFrame);
			}
			SafeRelease(pDepthFrameReference);
		}
		if (SUCCEEDED(hr))
		{
			int nDepthWidth = 0;
			int nDepthHeight = 0;
			UINT nDepthBufferSize = 0;
			UINT16*pDepthBuffer = NULL;
			//std::cout << "depth image create start" << std::endl;
			hr = pDepthFrame->AccessUnderlyingBuffer(&nDepthBufferSize, &pDepthBuffer);
			
			if (SUCCEEDED(hr)) {
				cv::Mat depthMap = cv::Mat(cDepthHeight, cDepthWidth, CV_16U, pDepthBuffer);
				depthMap.convertTo(mDepthMat, CV_8UC1, 255.0f / 8000.0f, 0.0f);
				//std::cout << "depth image create end" << std::endl;
			}
		}
		SafeRelease(pDepthFrame);
		SafeRelease(pMultiSourceFrame);
	}

	void mKinect::createContours(int threshold){	// contours list 만들기. depth mat
		// threshold
		cv::Mat thresholdMat(cDepthHeight, cDepthWidth, CV_8UC1);
		cv::Mat tempMat(cDepthHeight, cDepthWidth, CV_8UC3);
		cv::Mat cannyMat(cDepthHeight, cDepthWidth, CV_8UC3);
		cv::Mat adaptive(cDepthHeight, cDepthWidth, CV_8UC1);

		adaptive = mDepthMat.clone();

		for (int i = 0; i < mDepthMat.cols; ++i){
			for (int j = 0; j < mDepthMat.rows; ++j){
				if (threshold - 15 < *adaptive.ptr(j, i) && *adaptive.ptr(j, i) < threshold){
					*adaptive.ptr(j, i) = 0;
				}
				else{
					*adaptive.ptr(j, i) = 255;
				}
			}
		}
		//cv::threshold(mDepthMat, thresholdMat, threshold, 255, CV_THRESH_BINARY);
		cv::medianBlur(adaptive, thresholdMat, 5);

		/*cv::threshold(mDepthMat, thresholdMat, threshold, 255, CV_THRESH_BINARY);
		cv::medianBlur(thresholdMat, thresholdMat, 5);*/

		cv::cvtColor(thresholdMat, tempMat, CV_GRAY2BGR);


		cv::Canny(tempMat, cannyMat, 30, 128, 3, false); // contour 찾기위한 cannyedge 작업
		cv::findContours(cannyMat, contours, cv::RETR_EXTERNAL, cv::CHAIN_APPROX_SIMPLE); // contour 찾기
		cv::drawContours(tempMat, contours, -1, cv::Scalar(0, 0, 255), 1);				  // contour 그리기
		mDepthMat = adaptive.clone();
	}

	long mKinect::getContoursCenterLen(){ //contours center의 길이를 넘겨준다.
		return contours.size();
	}

	void mKinect::getContoursCenter(){	// contours center 를 넘겨준다.
		for (int i = 0; i < 255; ++i){
			mContoursCenter[i].x = 0;
			mContoursCenter[i].y = 0;
		}
		for (int i = 0; i < contours.size(); ++i){
			//std::cout << "사이즈 " << i << ": " << contours[i].size() << std::endl;
			int count_x = 0;
			int count_y = 0;
			for (int j = 0; j < contours[i].size(); ++j){
				if (0 <= contours[i][j].x && contours[i][j].x <= 512){
					mContoursCenter[i].x += contours[i][j].x;
					count_x += 1;
				}
				if (0 <= contours[i][j].y && contours[i][j].y < 424){
					mContoursCenter[i].y += contours[i][j].y;
					count_y += 1;
				}
			}
			if (count_x != 0)
				mContoursCenter[i].x = mContoursCenter[i].x / count_x;
			else
				mContoursCenter[i].x = 0;
			if (count_y != 0)
				mContoursCenter[i].y = mContoursCenter[i].y / count_y;
			else
				mContoursCenter[i].y = 0;
		}
	}

	bool mKinect::getCurrentFrame(){ /// 프레임 업데이트 하기.
		int count = 1;
		//std::cout << count++ << " 1번째" << std::endl;
		if (!m_pMultiSourceFrameReader)
		{
			return false;
		}

		IMultiSourceFrame* pMultiSourceFrame = NULL;
		IDepthFrame* pDepthFrame = NULL;
		IColorFrame* pColorFrame = NULL;
		IBodyIndexFrame* pBodyIndexFrame = NULL;

		HRESULT hr = m_pMultiSourceFrameReader->AcquireLatestFrame(&pMultiSourceFrame);
		//std::cout << count++ << " 4번째" << std::endl;
		if (SUCCEEDED(hr)){
			IDepthFrameReference*pDepthFrameReference = NULL;
			//std::cout << hr << "1오류임" << std::endl;
			hr = pMultiSourceFrame->get_DepthFrameReference(&pDepthFrameReference);
			if (SUCCEEDED(hr)){
				//std::cout << hr << "2오류임" << std::endl;
				hr = pDepthFrameReference->AcquireFrame(&pDepthFrame);
			}
			SafeRelease(pDepthFrameReference);
		}
		//std::cout << count++ << " 5번째" << std::endl;
		//std::cout << hr << "3오류임" << std::endl;
		if (SUCCEEDED(hr)){
			IColorFrameReference*pColorFrameReference = NULL;
			hr = pMultiSourceFrame->get_ColorFrameReference(&pColorFrameReference);
			//std::cout << hr << " 4오류임" << std::endl;
			if (SUCCEEDED(hr)){
				hr = pColorFrameReference->AcquireFrame(&pColorFrame);
			}
			SafeRelease(pColorFrameReference);
		}
		if (SUCCEEDED(hr))
		{
			IBodyIndexFrameReference* pBodyIndexFrameReference = NULL;

			hr = pMultiSourceFrame->get_BodyIndexFrameReference(&pBodyIndexFrameReference);
			if (SUCCEEDED(hr))
			{
				hr = pBodyIndexFrameReference->AcquireFrame(&pBodyIndexFrame);
			}

			SafeRelease(pBodyIndexFrameReference);
		}

		//std::cout << count++ << " 6번째" << std::endl;
		if (SUCCEEDED(hr)){
			INT64 nDepthTime = 0;
			IFrameDescription* pDepthFrameDescription = NULL;
			int nDepthWidth = 0;
			int nDepthHeight = 0;
			UINT nDepthBufferSize = 0;
			UINT16*pDepthBuffer = NULL;

			IFrameDescription*pColorFrameDescription = NULL;
			int nColorWidth = 0;
			int nColorHeight = 0;
			ColorImageFormat imageFormat = ColorImageFormat_None;
			UINT nColorBufferSize = 0;
			RGBQUAD*pColorBuffer = NULL;

			IFrameDescription*pBodyIndexFrameDescription = NULL;
			int nBodyIndexWidth = 0;
			int nBodyIndexHeight = 0;
			UINT nBodyIndexBufferSize = 0;
			BYTE*pBodyIndexBuffer = NULL;

			hr = pDepthFrame->get_RelativeTime(&nDepthTime);
			//std::cout << count++ << " 7번째" << std::endl;
			if (SUCCEEDED(hr)){
				hr = pDepthFrame->get_FrameDescription(&pDepthFrameDescription);
			}

			if (SUCCEEDED(hr)){
				hr = pDepthFrameDescription->get_Width(&nDepthWidth);
			}
			if (SUCCEEDED(hr)){
				hr = pDepthFrameDescription->get_Height(&nDepthHeight);
			}
			if (SUCCEEDED(hr))
			{
				std::cout << "real?" << std::endl;
				hr = pDepthFrame->AccessUnderlyingBuffer(&nDepthBufferSize, &pDepthBuffer);
				//hr = pDepthFrame->AccessUnderlyingBuffer(&nDepthBufferSize, reinterpret_cast<UINT16**>(&mDepthBufferMat.data));
				//memcpy(reinterpret_cast<UINT16**>(&mDepthBufferMat.data), &pDepthBuffer,nDepthBufferSize);
				if (SUCCEEDED(hr)) {
					cv::Mat depthMap = cv::Mat(cDepthHeight, cDepthWidth, CV_16U, pDepthBuffer);
					depthMap.convertTo(mDepthMat, CV_8UC1, 255.0f / 8000.0f, 0.0f);
				}
				/*if (SUCCEEDED(hr)) {
					cv::Mat depthMap = cv::Mat(height, width, CV_16U, depthBuffer);
					cv::Mat img0 = cv::Mat::zeros(height, width, CV_8UC1);
					cv::Mat img1;
					double scale = 255.0 / (nDepthMaxReliableDistance -
						nDepthMinReliableDistance);
					depthMap.convertTo(img0, CV_8UC1, scale);
					applyColorMap(img0, img1, cv::COLORMAP_JET);
					cv::imshow("Depth Only", img1);
				}*/
				/*hResult = pDepthFrame->AccessUnderlyingBuffer(&depthBufferSize, reinterpret_cast<UINT16**>(&depthBufferMat.data));
				if (SUCCEEDED(hResult)){
					depthBufferMat.convertTo(depthMat, CV_8U, -255.0f / 8000.0f, 255.0f);
				}*/

			}
			//std::cout << count++ << " 8번째" << std::endl;
			// get color frame data

			if (SUCCEEDED(hr)){
				hr = pColorFrame->get_FrameDescription(&pColorFrameDescription);
			}
			if (SUCCEEDED(hr)){
				hr = pColorFrameDescription->get_Width(&nColorWidth);
			}
			if (SUCCEEDED(hr)){
				hr = pColorFrameDescription->get_Height(&nColorHeight);
			}
			//std::cout << count++ << " 9번째" << std::endl;
			if (SUCCEEDED(hr)){
				if (imageFormat == ColorImageFormat_Bgra){
					hr = pColorFrame->AccessRawUnderlyingBuffer(&nColorBufferSize, reinterpret_cast<BYTE**>(&pColorBuffer));
					/*if (SUCCEEDED(hr)) {
						cv::Mat img(cColorHeight, cColorWidth, CV_8UC4,
							reinterpret_cast<void*>(pColorBuffer));
						mColorMat = img.clone();
					}*/
					//hr = pColorFrame->AccessRawUnderlyingBuffer(&nColorBufferSize, reinterpret_cast<BYTE**>(&mColorMat.data));
					//std::cout << count++ << " 10번째" << std::endl;
				}
				else if (m_pColorRGBX)
				{
					pColorBuffer = m_pColorRGBX;
					nColorBufferSize = cColorWidth * cColorHeight * sizeof(RGBQUAD);
					hr = pColorFrame->CopyConvertedFrameDataToArray(nColorBufferSize, reinterpret_cast<BYTE*>(pColorBuffer), ColorImageFormat_Bgra);
					/*if (SUCCEEDED(hr)) {
						cv::Mat img(cColorHeight, cColorWidth, CV_8UC4,
							reinterpret_cast<void*>(pColorBuffer));
						mColorMat = img.clone();
					}*/
					//hr = pColorFrame->CopyConvertedFrameDataToArray(nColorBufferSize, reinterpret_cast<BYTE*>(mColorMat.data), ColorImageFormat_Bgra);
					//std::cout << count++ << " 11번째" << std::endl;
				}
				else
				{
					hr = E_FAIL;
				}
			}
			//std::cout << count++ << " 12번째" << std::endl;
			if (SUCCEEDED(hr))
			{
				//std::cout << count++ << " 131번째" << std::endl;
				hr = pBodyIndexFrame->get_FrameDescription(&pBodyIndexFrameDescription);
				//std::cout << count++ << " 1111번째" << std::endl;
			}
			//std::cout << count++ << " 13번째" << std::endl;
			if (SUCCEEDED(hr))
			{
				hr = pBodyIndexFrameDescription->get_Width(&nBodyIndexWidth);
			}
			//std::cout << count++ << " 14번째" << std::endl;
			if (SUCCEEDED(hr))
			{
				hr = pBodyIndexFrameDescription->get_Height(&nBodyIndexHeight);
			}
			//std::cout << count++ << " 15번째" << std::endl;
			if (SUCCEEDED(hr))
			{
				hr = pBodyIndexFrame->AccessUnderlyingBuffer(&nBodyIndexBufferSize, &pBodyIndexBuffer);
			}
			//std::cout << count++ << " 16번째" << std::endl;
			if (SUCCEEDED(hr))
			{
				ProcessFrame(nDepthTime, pDepthBuffer, nDepthWidth, nDepthHeight,
					pColorBuffer, nColorWidth, nColorHeight,
					pBodyIndexBuffer, nBodyIndexWidth, nBodyIndexHeight);
			}
			//std::cout << count++ << " 17번째" << std::endl;
			SafeRelease(pDepthFrameDescription);
			SafeRelease(pColorFrameDescription);
			SafeRelease(pBodyIndexFrameDescription);
		}
		//std::cout << count++ << " 18번째" << std::endl;
		//cv::imshow("please", mColorMat);
		//std::cout << count++ << " 19번째" << std::endl;
		/*if (cv::waitKey(30) == VK_ESCAPE){
			return false;
		}*/
		//std::cout << count++ << " 20번째" << std::endl;
		SafeRelease(pDepthFrame);
		SafeRelease(pColorFrame);
		SafeRelease(pBodyIndexFrame);
		SafeRelease(pMultiSourceFrame);
		return true;
	}

}

TestKinect::mKinect val;

void KinectAPI::print(){
	val.print();
}

POINT** KinectAPI::getContours(){
	return val.getContours();
}

void KinectAPI::createimage(const char* path){
	val.mockupLoadimage(path);
}

unsigned char* KinectAPI::getShadowImage(){
	return val.getShadowImage();
}

void KinectAPI::updateContour(){
	val.updateContour();
}

int KinectAPI::getContoursSize(){
	return val.getContoursSize();
}

POINT* KinectAPI::getContourCenter(){
	return val.getContourCenter();
}

int*KinectAPI::getContourLen(){
	return val.getContourLen();
}

///////////////////////////////////////////////////////////////
bool KinectAPI::CreateShadowImage(int MaxImageCount){ // 만들어진 이미지의 개수를 저장할 변수를 넣어서 값을 대입해준다. 그리고 완벽하게 되었을 경우에 참을 넘겨준다.
	MaxImageCount = val.createShadowImage();
	return true;
}
POINT** KinectAPI::getImageContours(int num){ //
	POINT** list = nullptr;

	return list;
}
POINT* KinectAPI::getImageContoursCenter(int num){
	POINT* list = nullptr;

	return list;
}
POINT** KinectAPI::getTouchContours(){
	POINT** list = nullptr;
	return list;
}
int KinectAPI::InitKinect(){
	val.InitKinect();
	std::cout << "init kinect" << std::endl;
	return 1;
}

void KinectAPI::saveImage(){
	std::cout << "updateFrame" << std::endl;
	Sleep(30);
	//long temp;
	//val.getCurrentFrame(temp);
}

void KinectAPI::processIncomingData(){
	val.processIncomingData();
	val.print();
	//std::cout << "depth image print" << std::endl;
}

long CreateImage(){		// Image Create. File Dest current Folder
	Sleep(30);
	val.getCurrentFrame();
	return val.imagecount;
}

void InitKinect(){
	val.InitKinect();
	std::cout << "init Kinect Sensor" << std::endl;
}
void getContoursCenter(POINT*list, long len, long render){
	//getImageContoursCenter
	//POINT* mlist = val.getContoursCenter();	//공간이 확실해야됨!!!
	val.getContoursCenter();
	for (int i = 0; i < len; ++i){
		list[i].x = val.mContoursCenter[i].x;
		list[i].y = val.mContoursCenter[i].y;
	}
	/*for (int i = 0; i < len; ++i){
		std::cout << "mlist : " << mlist[i].x << " , " << mlist[i].y << std::endl;
	}
	for (int i = 0; i < len; ++i){
		std::cout << "list : " << list[i].x << " , " << list[i].y << std::endl;
	}

	if (mlist != nullptr){
		delete[] list;
	}*/
	if (render == 1){
		val.print();
	}
	//std::cout << "contours center clear" << std::endl;
}

long ContoursLen(){
	std::cout << val.getLen() << std::endl;
	return val.getLen();
}

void DepthImage(int threshold){
	val.getDepthImage();
	val.createContours(threshold);
}
long ContoursCenterLen(){
	//std::cout << val.getContoursCenterLen() << " : contours center len" << std::endl;
	return val.getContoursCenterLen();
}

