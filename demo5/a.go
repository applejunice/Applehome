package main

import (
	"context"
	"crypto/tls"
	"fmt"
	"io"
	"net"
	"net/http"
)

func main() {
	// 指定域名和 IP 地址
	domain := "bubble.freelink.co.jp"
	ipAddress := "162.159.35.39"

	// 创建自定义的 Transport，使用指定 IP 和域名
	transport := &http.Transport{
		TLSClientConfig: &tls.Config{
			ServerName:         domain, // SSL 握手时使用域名
			InsecureSkipVerify: true,   // 跳过证书验证（因为 IP 不匹配域名）
		},
		// 自定义 DialContext 函数，强制使用指定的 IP 地址
		DialContext: func(ctx context.Context, network, addr string) (net.Conn, error) {
			// 提取端口号
			_, port, err := net.SplitHostPort(addr)
			if err != nil {
				// 如果没有端口，默认使用 443
				port = "443"
			}
			// 强制连接到指定的 IP 地址
			dialer := &net.Dialer{}
			return dialer.DialContext(ctx, network, ipAddress+":"+port)
		},
	}

	// 创建 HTTP 客户端
	client := &http.Client{
		Transport: transport,
	}

	// 使用 IP 地址构建 URL
	reqURL := fmt.Sprintf("https://%s/", ipAddress)

	// 创建请求
	req, err := http.NewRequest("GET", reqURL, nil)
	if err != nil {
		fmt.Printf("创建请求失败: %v\n", err)
		return
	}

	// 设置 Host 头为域名
	req.Host = domain

	// 发送请求
	resp, err := client.Do(req)
	if err != nil {
		fmt.Printf("请求失败: %v\n", err)
		return
	}
	defer resp.Body.Close()

	// 读取响应体
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Printf("读取响应失败: %v\n", err)
		return
	}

	// 打印返回结果
	fmt.Printf("状态码: %d\n\n", resp.StatusCode)
	fmt.Println("响应头:")
	for key, values := range resp.Header {
		for _, value := range values {
			fmt.Printf("%s: %s\n", key, value)
		}
	}

	fmt.Println("\n响应内容:")
	fmt.Println(string(body))
}
