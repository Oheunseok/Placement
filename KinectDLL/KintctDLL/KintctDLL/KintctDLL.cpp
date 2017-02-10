// KintctDLL.cpp : DLL 응용 프로그램을 위해 내보낸 함수를 정의합니다.
//

#include "stdafx.h"
#include "testkinect.h"
#include "KinectAPI.h"
#include "BlobLabeling.h"

CBlobLabeling blob;
cv::Rect cutRect;


void CallBackFunc(int event, int x, int y, int flags, void* userdata)
{
	if (event == cv::EVENT_LBUTTONDOWN)
	{
		cutRect.x = x;
		cutRect.y = y;
		std::cout << "Left button of the mouse is clicked - position (" << x << ", " << y << ")" << std::endl;
	}
	else if (event == cv::EVENT_RBUTTONDOWN){
		cutRect.width = x - cutRect.x;
		cutRect.height = y - cutRect.y;
		std::cout << "Right button of the mouse is clicked - position (" << x << ", " << y << ")" << std::endl;
	}
}

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
		mColorCopyMat = cv::Mat(cColorHeight, cColorWidth, CV_8UC4); // 컬러 이미지가 나오게 하는 매트!.
		mDepthBufferMat = cv::Mat(cDepthHeight, cDepthWidth, CV_16UC1);
		mDepthMat = cv::Mat(cDepthHeight, cDepthWidth, CV_8UC1);
		mCoordinateMat = cv::Mat(cDepthHeight,cDepthWidth,CV_8UC4);

		mWhiteMat = cv::Mat(cColorHeight, cColorWidth, CV_8UC4);

		// create heap storage for composite image pixel data in RGBX format
		m_pOutputRGBX = new RGBQUAD[cColorWidth * cColorHeight];

		m_pColorFrameRGBX = new RGBQUAD[cColorWidth*cColorHeight];

		m_pWhiteFrameRGBX = new RGBQUAD[cColorWidth*cColorHeight];

		// create heap storage for background image pixel data in RGBX format
		m_pBackgroundRGBX = new RGBQUAD[cColorWidth * cColorHeight];

		// create heap storage for color pixel data in RGBX format
		m_pColorRGBX = new RGBQUAD[cColorWidth * cColorHeight];

		// create heap storage for the coorinate mapping from color to depth
		m_pDepthCoordinates = new DepthSpacePoint[cColorWidth * cColorHeight];

		depthBuffer = new UINT16[cDepthHeight * cDepthWidth];
		
		for (int i = 0; i < BGCOUNT; ++i){
			AddMat[i] = cv::Mat(cDepthHeight, cDepthWidth, CV_8UC1);
		}

		bgMat = cv::Mat(cDepthHeight, cDepthWidth, CV_8UC1);

		diffMat = cv::Mat(cDepthHeight, cDepthWidth, CV_8UC1);

		cv::namedWindow("Depth");
		cv::setMouseCallback("Depth", CallBackFunc, NULL);
	}

	mKinect::~mKinect(){
		std::cout << "kinect dtor" << std::endl; 

		if (m_pOutputRGBX)
		{
			delete[] m_pOutputRGBX;
			m_pOutputRGBX = NULL;
		}

		if (m_pColorFrameRGBX)
		{
			delete[] m_pColorFrameRGBX;
			m_pColorFrameRGBX = NULL;
		}

		if (m_pWhiteFrameRGBX)
		{
			delete[] m_pWhiteFrameRGBX;
			m_pWhiteFrameRGBX = NULL;
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
		cv::namedWindow("Depth");
		cv::setMouseCallback("Depth", CallBackFunc, NULL);
	}

	void mKinect::Finalize(){
		if (m_pOutputRGBX)
		{
			delete[] m_pOutputRGBX;
			m_pOutputRGBX = NULL;
		}

		if (m_pColorFrameRGBX)
		{
			delete[] m_pColorFrameRGBX;
			m_pColorFrameRGBX = NULL;
		}

		if (m_pWhiteFrameRGBX)
		{
			delete[] m_pWhiteFrameRGBX;
			m_pWhiteFrameRGBX = NULL;
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
		cv::imshow("Depth", mDepthMat);
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
		
		return 1;
	}

	void mKinect::updateTouchContour(){
		
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

				const RGBQUAD cwhite = { 255, 255, 255, 255 };
				// loop over output pixels
				for (int colorIndex = 0; colorIndex < (nColorWidth*nColorHeight); ++colorIndex)
				{
					// default setting source to copy from the background pixel
					const RGBQUAD* pSrc = m_pBackgroundRGBX + colorIndex;

					const RGBQUAD* pColorSrc = m_pBackgroundRGBX + colorIndex;

					const RGBQUAD* pWhiteSrc = m_pBackgroundRGBX + colorIndex;

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
								pColorSrc = m_pColorRGBX + colorIndex;
								pWhiteSrc = &cwhite;
							}
						}
					}

					// write output
					m_pOutputRGBX[colorIndex] = *pSrc;
					
					m_pColorFrameRGBX[colorIndex] = *pColorSrc;

					m_pWhiteFrameRGBX[colorIndex] = *pWhiteSrc;
				}
				cv::Mat img(cColorHeight, cColorWidth, CV_8UC4,
					reinterpret_cast<void*>(m_pOutputRGBX));
				mColorMat = img.clone();
				

				cv::Mat img1(cColorHeight, cColorWidth, CV_8UC4, reinterpret_cast<void*>(m_pColorFrameRGBX));
				mColorCopyMat = img1.clone();

				cv::Mat img2(cColorHeight, cColorWidth, CV_8UC4, reinterpret_cast<void*>(m_pWhiteFrameRGBX));
				mWhiteMat = img2.clone();

				cv::Mat colorFlip(cColorHeight, cColorWidth, CV_8UC4);
				cv::Mat whiteFlip(cColorHeight, cColorWidth, CV_8UC4);

				cv::flip(mColorCopyMat, colorFlip, 1);
				cv::flip(mWhiteMat, whiteFlip, 1);

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
					cv::Mat shadow_Tt;
					//mat(mrect).copyTo(saveImage);

					colorFlip(mrect).copyTo(saveImage);
					whiteFlip(mrect).copyTo(shadow_Tt);
					
					//shadow_Tt = ~shadow_Tt.clone();

					std::vector<int> compression_params;
					compression_params.push_back(CV_IMWRITE_PNG_COMPRESSION);
					compression_params.push_back(9);

					char buf[20];
					char tbuf[20];

					sprintf_s(buf, "picture%d.png", i);
					sprintf_s(tbuf, "spicture%d.png", i);

					//std::cout << buf << " create" << std::endl;

					try {
						imwrite(buf, saveImage, compression_params);
					}
					catch (std::runtime_error& ex) {
						fprintf(stderr, "Exception converting image to PNG format: %s\n", ex.what());
						return;
					}

					try {
						imwrite(tbuf, shadow_Tt, compression_params);
					}
					catch (std::runtime_error& ex) {
						fprintf(stderr, "Exception converting image to PNG format: %s\n", ex.what());
						return;
					}

				}
			}
		}

	}

	void mKinect::processIncomingData() {
		
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

		//mDepthMat(cutRect).copyTo(adaptive);

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

	void mKinect::createContoursDiffMat(){
		// threshold
		cv::Mat tempMat(cDepthHeight, cDepthWidth, CV_8UC3);
		cv::Mat cannyMat(cDepthHeight, cDepthWidth, CV_8UC3);
		cv::Mat adaptive(cDepthHeight, cDepthWidth, CV_8UC1);

		//adaptive = mDepthMat.clone();

		//cv::cvtColor(diffMat, tempMat, CV_GRAY2BGR);

		cv::Mat element5(5, 5, CV_8U, cv::Scalar(1));
		cv::morphologyEx(diffMat, diffMat, cv::MORPH_CLOSE, element5); // blur 처리한 이미지를 morphology연산하기, 노이즈 제거 작업.

		cv::Canny(diffMat, cannyMat, 30, 128, 3, false); // contour 찾기위한 cannyedge 작업
		cv::findContours(cannyMat, contours, cv::RETR_EXTERNAL, cv::CHAIN_APPROX_SIMPLE); // contour 찾기
	}

	long mKinect::getContoursCenterLen(){ //contours center의 길이를 넘겨준다.
		return contours.size();
	}

	void mKinect::KinectgetContours(POINT*list,long len){
		/*for (int i = 0; i < contours.size(); ++i){
			if (100 < contours[i].size())
				std::cout << i << " size : " << contours[i].size() << std::endl;
		}*/
		for (int i = 0; i < CONTOURSIZE * CONTOURLEN; ++i){
			list[i].x = 0;
			list[i].y = 0;
			
		}
		len = 0;
		for (int i = 0; i < contours.size(); ++i){
			if (CONTOURSIZE == i)
				break;
			for (int j = 0; j < contours[i].size(); ++j){
				if (j % 10 == 0 && j < CONTOURLEN){
					if (cutRect.x <= contours[i][j].x && contours[i][j].x <= cutRect.x + cutRect.width && cutRect.y <= contours[i][j].y && contours[i][j].y < cutRect.y + cutRect.height){
						list[len].x = contours[i][j].x;
						list[len].y = contours[i][j].y;
						
						len += 1;
					}
				}
			}
			
		}
		//std::cout << "len : " <<  len << std::endl;
		contoursCount = len;
	}

	void mKinect::getContoursCenter(){	// contours center 를 넘겨준다.
		for (int i = 0; i < contours.size(); ++i){
			if (100 < contours[i].size())
				std::cout << i << " size : " << contours[i].size() << std::endl;
		}
		for (int i = 0; i < 255; ++i){
			mContoursCenter[i].x = 0;
			mContoursCenter[i].y = 0;
		}
		for (int i = 0; i < contours.size(); ++i){
			//std::cout << "사이즈 " << i << ": " << contours[i].size() << std::endl;
			int count_x = 0;
			int count_y = 0;
			for (int j = 0; j < contours[i].size(); ++j){
				//if (cutRect.x /*0*/ <= contours[i][j].x && contours[i][j].x <= cutRect.x + cutRect.width /*512*/){
				//	mContoursCenter[i].x += contours[i][j].x;
				//	count_x += 1;
				//}
				//if (cutRect.y/*0*/ <= contours[i][j].y && contours[i][j].y < cutRect.y + cutRect.height/*424*/){
				//	mContoursCenter[i].y += contours[i][j].y;
				//	count_y += 1;
				//}
				if (cutRect.x /*0*/ <= contours[i][j].x && contours[i][j].x <= cutRect.x + cutRect.width /*512*/ && cutRect.y/*0*/ <= contours[i][j].y && contours[i][j].y < cutRect.y + cutRect.height/*424*/){
					mContoursCenter[i].x += contours[i][j].x;
					count_x += 1;
					mContoursCenter[i].y += contours[i][j].y;
					count_y += 1;
				}
			}
			if (count_x != 0){
				mContoursCenter[i].x = (float)((float)(mContoursCenter[i].x / count_x) - cutRect.x) / (cutRect.width) * cDepthWidth; // 지정한 범위를 바탕으로 컨투어 비율계산.
				//mContoursCenter[i].x = mContoursCenter[i].x / count_x;
				//std::cout << "x = " << mContoursCenter[i].x << std::endl;
			}
			else
				mContoursCenter[i].x = 0;
			if (count_y != 0){
				mContoursCenter[i].y = (float)((float)(mContoursCenter[i].y / count_y) - cutRect.y) / (cutRect.height) * cDepthHeight; // 지정한 범위를 바탕으로 컨투어 비율계산.
				//mContoursCenter[i].y = mContoursCenter[i].y / count_y;
				//std::cout << "y = " << mContoursCenter[i].y << std::endl;
			}
			else
				mContoursCenter[i].y = 0;
		}
	}

	void mKinect::CreateBG(){
		int bgcount = 0;

		while (bgcount != BGCOUNT){
			std::cout << bgcount << " 번 돌았음" << std::endl;
			Sleep(60);
			if (!m_pMultiSourceFrameReader)
			{
				std::cout << "multisourceFrameReader nullptr" << std::endl;
				return;
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

					AddMat[bgcount] = mDepthMat;

					bgcount += 1;
					//std::cout << "depth image create end" << std::endl;
				}
			}
			SafeRelease(pDepthFrame);
			SafeRelease(pMultiSourceFrame);
		}
		for (int i = 0; i < cDepthHeight; ++i){
			for (int j = 0; j < cDepthWidth; ++j){
				int value = 0;
				for (int index = 0; index < BGCOUNT; ++index){
					value += *AddMat[index].ptr(i, j);
				}
				*bgMat.ptr(i, j) = value / BGCOUNT;
			}
		}
	}

	long mKinect::CheckBG(const char*filename){

		const char buf[20] = "bg.png";
		cv::Mat bg = cv::imread(buf);
		std::cout << buf << " this name " << std::endl;
		if (bg.cols <= 0 || bg.rows <= 0){ // 기준 평균 배경화면이 없을때. 생성을 하자.
			int bgcount = 0;
			while (bgcount != BGCOUNT){
				std::cout << bgcount << " 번 돌았음" << std::endl;
				Sleep(60);
				if (!m_pMultiSourceFrameReader)
				{
					std::cout << "multisourceFrameReader nullptr" << std::endl;
					return 0;
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

						AddMat[bgcount] = mDepthMat;

						bgcount += 1;
						//std::cout << "depth image create end" << std::endl;
					}
				}
				SafeRelease(pDepthFrame);
				SafeRelease(pMultiSourceFrame);
			}
			for (int i = 0; i < cDepthHeight; ++i){
				for (int j = 0; j < cDepthWidth; ++j){
					int value = 0;
					for (int index = 0; index < BGCOUNT; ++index){
						value += *AddMat[index].ptr(i, j);
					}
					*bgMat.ptr(i, j) = value / BGCOUNT;
				}
			}
			std::cout << "file create before" << std::endl;
			//bg = bgMat.clone();
			//std::cout << filepath << " read fail. create file " << filepath << std::endl;
			/*std::vector<int> compression_params;
			compression_params.push_back(CV_IMWRITE_PNG_COMPRESSION);
			compression_params.push_back(9);*/

			//return false;
			//char buf[20];
			//sprintf_s(buf, "picture.png");
			try {
				//std::cout << "this error" << std::endl;
				cv::imwrite(buf, bgMat);
			}
			catch (std::runtime_error& ex) {
				fprintf(stderr, "Exception converting image to PNG format: %s\n", ex.what());
				std::cout << "bgImage file create error" << std::endl;
				return 0;
			}
			std::cout << "file create after" << std::endl;
		}
		else{
			Sleep(7000);
			//CreateBG();
			bgMat = cv::imread(buf);
			std::cout << "bgMat Data" << std::endl;
			std::cout << "cols : " << bgMat.cols << "rows : " << bgMat.rows << std::endl;
		}
		return 1;
	}

	void mKinect::AddBackGround(){
		
	}

	void mKinect::DiffMat(){
		std::cout << "here 1" << std::endl;
		cv::absdiff(mDepthMat, bgMat, diffMat);
		//cv::absdiff(bgMat, mDepthMat, diffMat);
		std::cout << "here 22" << std::endl;
		for (int i = 0; i < cDepthHeight; ++i){
			for (int j = 0; j < cDepthWidth; ++j){
				if (2 < *diffMat.ptr(i, j) && *diffMat.ptr(i, j) < 20){
					*diffMat.ptr(i, j) = 0;
				}
				else{
					*diffMat.ptr(i, j) = 255;
				}
			}
		}
	}

	long mKinect::getContoursLen(){
		return contours.size();
	}

	void mKinect::contoursRect(POINT*center,POINT*r){		//비율 조절합ㄴ시다.
		int count = 0;
		for (int i = 0; i < contours.size(); ++i){
			int minx = 10000;
			int miny = 10000;
			int maxx = 0;
			int maxy = 0;
			bool create = false;
			for (int j = 0; j < contours[i].size(); ++j){
				if (cutRect.x /*0*/ <= contours[i][j].x && contours[i][j].x <= cutRect.x + cutRect.width /*512*/ && cutRect.y/*0*/ <= contours[i][j].y && contours[i][j].y < cutRect.y + cutRect.height/*424*/){
					create = true;
					contours[i][j].x = (float)((float)(contours[i][j].x) - cutRect.x) / (cutRect.width) * cDepthWidth;
					contours[i][j].y = (float)((float)(contours[i][j].y) - cutRect.y) / (cutRect.height) * cDepthHeight;

					if (maxx <= contours[i][j].x){
						maxx = contours[i][j].x;
					}

					if (contours[i][j].x <= minx){
						minx = contours[i][j].x;
					}

					if (maxy <= contours[i][j].y){
						maxy = contours[i][j].y;
					}

					if (contours[i][j].y <= miny){
						miny = contours[i][j].y;
					}
				}
			}
			if (create){
				center[count].x = (maxx - minx) / 2 + minx;
				center[count].y = (maxy - miny) / 2 + miny;

				r[count].x = (maxx - minx) / 2;
				r[count].y = (maxy - miny) / 2;
				count += 1;
			}
			std::cout << "center = " << center[i].x << " " << center[i].y << std::endl;
			std::cout << "r = " << r[i].x << " " << r[i].y << std::endl;
		}

		//contoursCount = contours.size();
		rectCount = count;
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
	val.createContoursDiffMat();
	val.getContoursCenter();
	for (int i = 0; i < len; ++i){
		list[i].x = val.mContoursCenter[i].x;
		list[i].y = val.mContoursCenter[i].y;
	}
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

void CreateRect(){
	val.getDepthImage();
	val.print();
}

void DepthImageUpdate(){
	val.getDepthImage();
	std::cout << "hello1" << std::endl;
	val.DiffMat();
	std::cout << "hello2" << std::endl;
	//val.createContoursDiffMat();
}

void BGCreate(){
	val.CreateBG();
}

long CheckBG(){
	return val.CheckBG("aa");
}

long getContoursLen(){	//contours 넘기는
	return val.contoursCount;
}
void getContours(POINT*list, long len, long render){
	val.createContoursDiffMat();
	val.KinectgetContours(list,len);
}

void closeCVwindow(){
	val.closeWindow();
}

void getContoursRect(POINT*center, POINT*r){
	val.createContoursDiffMat();
	val.contoursRect(center, r);
	center[0].x = 100;
	center[0].y = 200;
}

long getContourRectCount(){
	return val.rectCount;
}

////////////////////////////////////////////////// unity test
int unityReturnint(){
	int ret = 10;
	return ret;
}
int* unityReturnintPointer(){
	int arr[10];
	for (int i = 0; i < 10; ++i){
		arr[i] = i;
	}
	return arr;
}

void unityGetPOINT(POINT* list){
	for (int i = 0; i < 10; ++i){
		list[i].x = i;
		list[i].y = i;
	}
}
POINT* unityReturnPOINT(){
	POINT* arr = new POINT[10];
	for (int i = 0; i < 10; ++i){
		arr[i].x = i;
		arr[i].y = i;
	}
	return arr;
}

int init(){
	return val.InitKinect();
}

int closeKinect(){
	val.Finalize();
	return 1;
}

POINT getRectWidth(){
	POINT a;
	a.x = cutRect.width;
	a.y = cutRect.height;
	return a;
}

void UnityRect(POINT*center, POINT*r){
	val.createContoursDiffMat();
	//val.contoursRect(center, r);
	int count = 0;
	for (int i = 0; i < val.contours.size(); ++i){
		int minx = 10000;
		int miny = 10000;
		int maxx = 0;
		int maxy = 0;
		bool create = false;
		for (int j = 0; j < val.contours[i].size(); ++j){
			if (cutRect.x /*0*/ <= val.contours[i][j].x && val.contours[i][j].x <= cutRect.x + cutRect.width /*512*/ && cutRect.y/*0*/ <= val.contours[i][j].y && val.contours[i][j].y < cutRect.y + cutRect.height/*424*/){
				create = true;
				val.contours[i][j].x = (float)((float)(val.contours[i][j].x) - cutRect.x) / (cutRect.width) * 512;
				val.contours[i][j].y = (float)((float)(val.contours[i][j].y) - cutRect.y) / (cutRect.height) * 424;

				if (maxx <= val.contours[i][j].x){
					maxx = val.contours[i][j].x;
				}

				if (val.contours[i][j].x <= minx){
					minx = val.contours[i][j].x;
				}

				if (maxy <= val.contours[i][j].y){
					maxy = val.contours[i][j].y;
				}

				if (val.contours[i][j].y <= miny){
					miny = val.contours[i][j].y;
				}
			}
		}
		if (create){
			center[count].x = (maxx - minx) / 2 + minx;
			center[count].y = (maxy - miny) / 2 + miny;

			r[count].x = (maxx - minx) / 2;
			r[count].y = (maxy - miny) / 2;
			count += 1;
		}
		std::cout << "center = " << center[i].x << " " << center[i].y << std::endl;
		std::cout << "r = " << r[i].x << " " << r[i].y << std::endl;
	}

	//contoursCount = contours.size();
	val.rectCount = count;
}

int getRectCount(){
	return val.rectCount;
}